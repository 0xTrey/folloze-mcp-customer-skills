"""Synthetic native rule and readback regressions. No Folloze connection."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('native_contract', ROOT / 'Skills/folloze-native-one-to-few-campaign-page/scripts/native_contract.py')
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)


class NativeContractTests(unittest.TestCase):
    def setUp(self):
        self.rules = json.loads((ROOT / 'Skills/folloze-native-one-to-few-campaign-page/examples/industry-account-contract.json').read_text())

    def test_native_fixture_and_all_recognition_combinations(self):
        self.assertEqual(native.errors(self.rules), [])
        cases = [(None,None,None,'generic',None,'your team'),('Financial Services',None,None,'banking',None,'your team'),(None,'bank.example','Acme','generic','approved-bank-logo','Acme'),('Pharmaceuticals','bank.example','Acme','pharma','approved-bank-logo','Acme'),('Unknown','other.example',None,'generic',None,'your team')]
        for industry,domain,name,variant,logo,callout in cases:
            result = native.resolve_view(self.rules,industry=industry,domain=domain,account_name=name)
            self.assertEqual((result['variant'],result['logo'],result['account_callout_text']),(variant,logo,callout))
            self.assertEqual(result['evidence'],'expected_only')

    def test_unknown_or_malformed_identity_is_generic(self):
        for value in (None,[],{},42,' financial services '):
            result=native.resolve_view(self.rules,industry=value,domain=value,account_name=value)
            self.assertEqual(result['variant'],'generic')
            self.assertIsNone(result['logo'])

    def test_account_text_is_preserved_without_html_execution(self):
        name="O'Brien & Partners <team>"
        result=native.resolve_view(self.rules,account_name=name)
        self.assertEqual(result['account_callout_text'],name)
        self.assertNotIn('html',result)

    def test_domain_cannot_change_message(self):
        self.rules['logo_rules'][0]['effects']['hero']='Banking copy'
        self.assertIn('changes messaging',';'.join(native.errors(self.rules)))

    def test_logo_header_diff_cannot_change_cta(self):
        self.rules['logo_rules'][0]['header_without_logo']={'cta':'Different offer'}
        self.assertIn('non-logo header',';'.join(native.errors(self.rules)))

    def test_industry_cannot_use_domain_field(self):
        self.rules['industry_rules'][0]['field_id']='domain-field'
        self.assertIn('industry field',';'.join(native.errors(self.rules)))

    def test_unavailable_industry_value_rejected(self):
        self.rules['industry_rules'][0]['value']='Banking guess'
        self.assertIn('not supported',';'.join(native.errors(self.rules)))

    def test_unreachable_variant_rejected(self):
        self.rules['industry_rules'].pop()
        self.assertIn('must have an industry condition',';'.join(native.errors(self.rules)))

    def test_malformed_domain_configuration_rejected(self):
        self.rules['logo_rules'][0]['domain']='bad..example'
        self.assertIn('exact domain',';'.join(native.errors(self.rules)))

    def test_duplicate_condition_rejected(self):
        self.rules['industry_rules'].append(copy.deepcopy(self.rules['industry_rules'][0]))
        self.assertIn('ambiguous',';'.join(native.errors(self.rules)))

    def test_generic_variant_must_be_complete(self):
        del self.rules['variants']['generic']['sections']['leading']
        self.assertIn('incomplete section',';'.join(native.errors(self.rules)))

    def test_dynamic_leading_id_is_not_manual_selection(self):
        self.rules['variants']['banking']['leading']['selection']='dynamic'
        self.assertIn('explicit selection',';'.join(native.errors(self.rules)))

    def test_token_must_match_discovery(self):
        self.rules['account_token']['syntax']='{{company}}'
        self.assertIn('differs from discovery',';'.join(native.errors(self.rules)))

    def test_missing_anonymous_token_fallback_rejected(self):
        self.rules['account_token']['fallback']='{!account_name}'
        self.assertIn('anonymous fallback',';'.join(native.errors(self.rules)))

    def test_each_industry_banner_needs_a_name_callout(self):
        self.rules['variants']['banking']['sections']['hero']['headline']='Banking operations'
        self.assertIn('lacks the account-name callout',';'.join(native.errors(self.rules)))

    def test_account_strip_alone_cannot_satisfy_banner_callout(self):
        self.rules['account_token']['placement']='separate_account_strip'
        self.assertIn('inside each industry banner',';'.join(native.errors(self.rules)))

    def test_banner_images_and_messages_cannot_repeat(self):
        for field in ('image','headline'):
            with self.subTest(field=field):
                rules=copy.deepcopy(self.rules)
                rules['variants']['pharma']['sections']['hero'][field]=rules['variants']['banking']['sections']['hero'][field]
                self.assertIn('must differ in every view',';'.join(native.errors(rules)))

    def test_no_name_banner_must_not_expose_token(self):
        self.rules['variants']['banking']['sections']['hero']['fallback_headline']='For {!account_name}'
        self.assertIn('complete no-name headline',';'.join(native.errors(self.rules)))

    def test_domain_logo_presentation_preserves_messaging(self):
        self.rules['logo_rules'][0]['effects'].update(secondary_logo_visible=True,secondary_logo_scale=0.8,separator_visible=True)
        self.assertEqual(native.errors(self.rules),[])

    def test_saved_banner_drift_is_rejected(self):
        readback=copy.deepcopy(self.rules)
        readback['variants']['banking']['sections']['hero']['image']='stale-image'
        self.assertIn('banner imagery/messaging/callout readback mismatch',';'.join(native.readback_errors(self.rules,readback)))

    def test_item_ownership_and_blank_pdf_rejected(self):
        self.rules['items']['pdf-banking']['board_id']='other-board'
        self.rules['items']['pdf-pharma']['file_id']=None
        errors=';'.join(native.errors(self.rules))
        self.assertIn('wrong board',errors);self.assertIn('incomplete PDF',errors)

    def test_readback_matches_items_and_native_bindings(self):
        readback=copy.deepcopy(self.rules)
        for item in readback['items'].values():
            if item['type']=='pdf':item['reader_pages']=item['expected_pages']
        self.assertEqual(native.readback_errors(self.rules,readback),[])
        readback['variants']['banking']['leading']['item_id']='pdf-generic'
        readback['items']['pdf-pharma']['reader_pages']=1
        result=';'.join(native.readback_errors(self.rules,readback))
        self.assertIn('binding mismatch',result);self.assertIn('page count mismatch',result)

    def test_saved_rule_drift_is_not_hidden_by_correct_items(self):
        readback=copy.deepcopy(self.rules)
        readback['industry_rules'][0]['field_id']='domain-field'
        self.assertIn('saved rule/identity', ';'.join(native.readback_errors(self.rules,readback)))


if __name__ == '__main__':
    unittest.main()
