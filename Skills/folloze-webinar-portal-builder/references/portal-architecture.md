# Webinar Portal Architecture

Choose the smallest structure that lets attendees find the right live or on-demand session without losing context.

## Experience Shapes

| Mode | Minimum event count | Default structure | Best use |
| --- | ---: | --- | --- |
| `single_event_lifecycle` | 1 | one event surface plus resources and next action | registration, live companion, replay transition |
| `series_hub` | 2 | series overview plus direct event routes | recurring or themed webinar programs |
| `webinar_platform` | 3 | featured event, upcoming/live/on-demand grouping, filters or navigation, resource library | reusable demo portal or ongoing event destination |

Do not add pages merely to make the portal feel larger. Direct event links must preserve a clear route back to the hub.

## Default Modules

### Single event

1. Header and concise event navigation.
2. Primary headline, lifecycle metadata, and one action.
3. Live provider surface or accurate external route with fallback.
4. Outcomes or agenda.
5. Verified speaker module when speakers are approved.
6. Five or six supporting resources.
7. Next useful action.

### Series hub

1. Series promise and next session.
2. Upcoming, live, and on-demand session cards with unambiguous state.
3. Direct event routes.
4. Shared speaker, topic, or role navigation when useful.
5. Curated resource library.
6. Series subscription, workshop, or conversation action when approved.

### Webinar platform

1. Platform promise and featured session.
2. Upcoming and live area.
3. On-demand library with usable filtering or grouping.
4. Event detail routes with provider and fallback behavior.
5. Shared resource library.
6. Clear next action.

## Visual Hierarchy

Start with one primary headline. Do not place a small eyebrow or kicker above it and an explanatory dek below it. Put date, time, lifecycle, audience context, and supporting copy in a metadata block, schedule module, caption, or body section.

Use source-owned event imagery, speaker photography, product visuals, diagrams, or restrained brand composition. Avoid generic conference-stage imagery and decorative dashboard clutter.

## Provider Routing

Supported manifest providers include Zoom Meeting, Zoom Webinar, ON24, Vimeo Live, YouTube Live, and an external live provider. Provider support in the manifest does not prove a matching native Folloze component.

Use `native_widget` only when current capability discovery proves:

- provider support for the intended event type
- real component tag and data shape
- destination and scheduling fields
- pre-live, live, and post-live behavior
- mobile behavior
- a safe direct fallback

If any item is missing, use `external_link` or `companion_only`. Do not use arbitrary iframe code as a substitute for capability evidence.

## Registration Routes

- `provider_registration`: primary action opens the verified provider registration page.
- `folloze_then_provider`: a board-owned Folloze form redirects to provider registration. This is a two-step flow.
- `direct_join_after_registration`: use only for an approved non-personal join destination and the intended access model.
- `none`: valid only when the active lifecycle does not require registration.

Never describe a Folloze form submission as completed provider registration unless a verified integration actually completes it.
