#!/usr/bin/env python3
"""Offline validation and expected-view resolution. No network or Folloze writes."""
from __future__ import annotations
import argparse
import copy
import json
import re
from pathlib import Path


def errors(contract: dict) -> list[str]:
    if not isinstance(contract, dict):
        return ['Contract must be an object']
    out = []
    caps = contract.get('capabilities', {})
    if not caps.get('receipt') or not caps.get('observed_at'):
        out.append('capabilities need a dated discovery receipt')
    fields = {str(f['id']): f for f in caps.get('fields', [])}
    required = set(contract.get('required_roles', []))
    variants = contract.get('variants', {})
    if 'generic' not in variants:
        out.append('generic variant is required')
    for key, view in variants.items():
        if not required <= set(view.get('sections', {})):
            out.append(f'{key}: incomplete section roles')
        if any(not value for value in view.get('sections', {}).values()):
            out.append(f'{key}: empty section content')
        lead = view.get('leading', {})
        if lead.get('selection') != 'manual' or not lead.get('item_id'):
            out.append(f'{key}: leading item must have explicit selection and item ID')
    seen = set()
    mapped, field_ids = set(), set()
    for rule in contract.get('industry_rules', []):
        mapped.add(rule.get('variant')); field_ids.add(str(rule.get('field_id')))
        field = fields.get(str(rule.get('field_id')), {})
        if field.get('semantic') != 'industry' or not field.get('enabled'):
            out.append('industry rule must use a discovered enabled industry field')
        if rule.get('value') not in field.get('allowed_values', []):
            out.append('industry value is not supported by discovery')
        if rule.get('variant') not in variants or rule.get('variant') == 'generic':
            out.append('industry rule has no distinct variant')
        signature = (str(rule.get('field_id')), rule.get('value'))
        if signature in seen:
            out.append('ambiguous industry condition')
        seen.add(signature)
    if mapped != set(variants) - {'generic'}:
        out.append('every non-generic variant must have an industry condition')
    if len(field_ids) != 1:
        out.append('choose one discovered industry provider or define a separate precedence model')
    header = contract.get('header', {})
    domains = set()
    for rule in contract.get('logo_rules', []):
        field = fields.get(str(rule.get('field_id')), {})
        if field.get('semantic') != 'account_domain' or not field.get('enabled'):
            out.append('logo rule must use a discovered enabled domain field')
        domain = rule.get('domain', '')
        if not isinstance(domain, str) or not re.fullmatch(r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}', domain):
            out.append('logo rule needs an exact domain, not a URL or address')
        if domain in domains:
            out.append('duplicate domain rule')
        domains.add(domain)
        if set(rule.get('effects', {})) - {'secondary_logo', 'secondary_logo_visible', 'secondary_logo_scale', 'separator_visible'}:
            out.append('logo-only domain rule changes messaging')
        if not rule.get('effects', {}).get('secondary_logo'):
            out.append('logo rule has no logo')
        if rule.get('header_without_logo', header) != header:
            out.append('logo override changes non-logo header fields')
    token = contract.get('account_token', {})
    field = fields.get(str(token.get('field_id')), {})
    if field.get('semantic') != 'account_name' or not field.get('enabled') or not field.get('replacement'):
        out.append('account token requires a discovered replacement-capable field')
    if not token.get('syntax') or token.get('syntax') != field.get('token'):
        out.append('account token syntax differs from discovery')
    if not token.get('fallback') or '{!' in token.get('fallback', ''):
        out.append('account token needs literal-free anonymous fallback')
    if token.get('placement') != 'inside_each_industry_banner':
        out.append('account callout must be inside each industry banner')
    headlines, images = set(), set()
    for key, view in variants.items():
        hero = view.get('sections', {}).get('hero', {})
        if not isinstance(hero, dict) or not hero.get('headline') or not hero.get('image'):
            out.append(f'{key}: banner needs a headline and image')
            continue
        headline, image = hero['headline'], hero['image']
        if not isinstance(headline, str) or not isinstance(image, str):
            out.append(f'{key}: banner headline and image must be strings')
            continue
        if headline in headlines or image in images:
            out.append(f'{key}: banner messaging and imagery must differ in every view')
        headlines.add(headline); images.add(image)
        if key == 'generic':
            if token.get('syntax') and token['syntax'] in headline:
                out.append('generic: banner must not expose an account token')
        else:
            if not token.get('syntax') or token['syntax'] not in headline:
                out.append(f'{key}: industry banner lacks the account-name callout')
            fallback = hero.get('fallback_headline')
            if not isinstance(fallback, str) or not fallback.strip() or (token.get('syntax') and token['syntax'] in fallback):
                out.append(f'{key}: banner needs a complete no-name headline')
    items = contract.get('items', {})
    for key, view in variants.items():
        ids = [view.get('leading', {}).get('item_id')] + view.get('resources', [])
        if not view.get('resources'):
            out.append(f'{key}: empty resource list')
        for item_id in ids:
            if str(item_id) not in items:
                out.append(f'{key}: unresolved native item {item_id}')
    for item_id, item in items.items():
        if item.get('board_id') != contract.get('board_id') or not item.get('title') or not item.get('source'):
            out.append(f'{item_id}: missing provenance or wrong board')
        if item.get('type') == 'pdf' and (not item.get('file_id') or not item.get('sha256') or not item.get('expected_pages')):
            out.append(f'{item_id}: incomplete PDF import ledger')
    return out


def resolve_view(contract: dict, *, industry=None, domain=None, account_name=None) -> dict:
    """Expected contract result, never a runtime recognition receipt."""
    problems = errors(contract)
    if problems:
        raise ValueError('; '.join(problems))
    key = next((r['variant'] for r in contract['industry_rules'] if isinstance(industry, str) and r['value'] == industry), 'generic')
    logo = next((r['effects']['secondary_logo'] for r in contract['logo_rules'] if isinstance(domain, str) and r['domain'] == domain), None)
    name = account_name.strip() if isinstance(account_name, str) else ''
    return {'variant': key, 'view': copy.deepcopy(contract['variants'][key]), 'logo': logo,
            'account_callout_text': name or contract['account_token']['fallback'], 'evidence': 'expected_only'}


def readback_errors(contract: dict, readback: dict) -> list[str]:
    out = []
    for field in ('board_id', 'industry_rules', 'logo_rules', 'account_token', 'header'):
        if readback.get(field) != contract.get(field):
            out.append(f'{field}: saved rule/identity readback mismatch')
    for item_id, expected in contract['items'].items():
        actual = readback.get('items', {}).get(item_id, {})
        for field in ('board_id', 'title', 'type', 'file_id'):
            if field in expected and actual.get(field) != expected[field]:
                out.append(f'{item_id}: {field} readback mismatch')
        if expected.get('type') == 'pdf' and actual.get('reader_pages') != expected['expected_pages']:
            out.append(f'{item_id}: reader page count mismatch or unverified')
    for key, view in contract['variants'].items():
        actual = readback.get('variants', {}).get(key, {})
        if actual.get('sections', {}).get('hero') != view.get('sections', {}).get('hero'):
            out.append(f'{key}: banner imagery/messaging/callout readback mismatch')
        if actual.get('leading') != view['leading'] or actual.get('resources') != view['resources']:
            out.append(f'{key}: leading/resource binding mismatch')
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('contract', type=Path)
    parser.add_argument('--readback', type=Path)
    args = parser.parse_args()
    try:
        contract = json.loads(args.contract.read_text())
        problems = errors(contract)
        if args.readback and not problems:
            problems += readback_errors(contract, json.loads(args.readback.read_text()))
    except (ValueError, OSError, TypeError, KeyError) as exc:
        problems = [str(exc)]
    print(json.dumps({'status': 'fail' if problems else 'pass', 'scope': 'offline_contract_only', 'errors': problems}, indent=2))
    return bool(problems)


if __name__ == '__main__':
    raise SystemExit(main())
