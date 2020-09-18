# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog], and this project adheres to
[Semantic Versioning]. The file is auto-generated using [Conventional Commits].

[keep a changelog]: https://keepachangelog.com/en/1.0.0/
[semantic versioning]: https://semver.org/spec/v2.0.0.html
[conventional commits]: https://www.conventionalcommits.org/en/v1.0.0/

## Overview
- [`0.1.5`](#015) – _2020.09.18_
- [`0.1.4`](#014) – _2020.09.17_
- [`0.1.3`](#013) – _2020.09.15_
- [`0.1.2`](#012) – _2020.08.17_
- [`0.1.1`](#011) – _2020.08.14_
- [`0.1.0`](#010) – _2020.08.10_

## [0.1.5]

_2020.09.18_

### Contributions

This release is made possible by the following people (in alphabetical order).
Thank you all for your contributions. Your work – no matter how significant – is
greatly appreciated by the community. 💖

- Jan Christian Grünhage (<jan.christian@gruenhage.xyz>)

### Changes

#### Synapse Role

##### Updates

- **bump version to 1.19.3** ([`a23c007`])


## [0.1.4]

_2020.09.17_

### Contributions

This release is made possible by the following people (in alphabetical order).
Thank you all for your contributions. Your work – no matter how significant – is
greatly appreciated by the community. 💖

- Jan Christian Grünhage (<jan.christian@gruenhage.xyz>)

### Changes

#### Synapse Role

##### Updates

- **bump version to 1.19.2** ([`d73cde6`])


## [0.1.3]

_2020.09.15_

### Contributions

This release is made possible by the following people (in alphabetical order).
Thank you all for your contributions. Your work – no matter how significant – is
greatly appreciated by the community. 💖

- Jan Christian Grünhage (<jan.christian@gruenhage.xyz>)

### Changes

#### Synapse Role

##### Documentation

- **fix markdown tables in README** ([`4290448`])

##### Updates

- **bump version to 1.19.1** ([`cc0e081`])


#### Element Role

##### Updates

- **bump version to 1.7.7** ([`5d20369`])


## [0.1.2]

_2020.08.17_

### Contributions

This release is made possible by the following people (in alphabetical order).
Thank you all for your contributions. Your work – no matter how significant – is
greatly appreciated by the community. 💖

- Jan Christian Grünhage (<jan.christian@gruenhage.xyz>)

### Changes

#### Element Role

##### Updates

- **bump version to 1.7.4** ([`16e1ecb`])


#### Synapse Role

##### Updates

- **bump version to 1.19.0** ([`859b388`])


## [0.1.1]

_2020.08.14_

### Contributions

This release is made possible by the following people (in alphabetical order).
Thank you all for your contributions. Your work – no matter how significant – is
greatly appreciated by the community. 💖

- Jan Christian Grünhage (<jan.christian@gruenhage.xyz>)

### Changes

#### Element Role

##### Bug Fixes

- **change folder name to match artifact** ([`a76ebb1`])

  During the renaming of Riot to Element, the path for the webapp changed
  from /opt/riot to /opt/element. In those folders, the archives are
  unpacked, resulting in paths like /opt/element/riot-v${version}. Since
  the archives are not yet renamed
  (https://github.com/vector-im/element-web/issues/14896), this riot
  reference has to stay for now. In the renaming, this was accidentally
  changed prematurely, resulting in this regression.


## [0.1.0]

_2020.08.10_

### Contributions

This release is made possible by the following people (in alphabetical order).
Thank you all for your contributions. Your work – no matter how significant – is
greatly appreciated by the community. 💖

- Jan Christian Grünhage (<jan.christian@gruenhage.xyz>)

### Changes

#### Element Role

##### Updates

- **bump version to 1.7.3** ([`e2fbaf6`])

##### Refactoring

- **rename riot role to element** ([`5a777cd`])

  Riot is now Element, and therefore this role has to do a lot of
  `s/riot/element/g`. There's still a few references to riot here and
  there, but fixing those depends on external changes.

  This does not attempt any automatic migration, you will need to clean
  up the old webroot or container yourself.


#### Synapse Role

##### Bug Fixes

- **fix location of signing key module** ([`40510a6`])

##### Updates

- **bump version to 1.18.0** ([`d1edba8`])


#### Riot Role

##### Updates

- **bump version to 1.7.2** ([`6be0252`])



<!--
Config(
  accept_types: ["feat", "fix", "update", "refactor", "docs"],
  type_headers: {
    "feat": "Features",
    "fix": "Bug Fixes",
    "update": "Updates",
    "refactor": "Refactoring",
    "docs": "Documentation"
  },
  scope_headers: {
    "synapse": "Synapse Role",
    "element": "Element Role",
    "riot": "Riot Role"
  }
)
Template(
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog], and this project adheres to
[Semantic Versioning]. The file is auto-generated using [Conventional Commits].

[keep a changelog]: https://keepachangelog.com/en/1.0.0/
[semantic versioning]: https://semver.org/spec/v2.0.0.html
[conventional commits]: https://www.conventionalcommits.org/en/v1.0.0/

## Overview

{%- for release in releases %}
- [`{{ release.version }}`](#{{ release.version | replace(from=".", to="") }}) – _{{ release.date | date(format="%Y.%m.%d")}}_
{%- endfor %}

{% for release in releases -%}
## [{{ release.version }}]

_{{ release.date | date(format="%Y.%m.%d") }}_
{%- if release.notes %}

{{ release.notes }}
{% endif -%}
{%- if release.changeset.contributors %}

### Contributions

This release is made possible by the following people (in alphabetical order).
Thank you all for your contributions. Your work – no matter how significant – is
greatly appreciated by the community. 💖
{% for contributor in release.changeset.contributors %}
- {{ contributor.name }} (<{{ contributor.email }}>)
{%- endfor %}
{%- endif %}

### Changes

{% for scope, changes in release.changeset.changes | group_by(attribute="scope") -%}

#### {{ scope | scopeheader }}

{% for type, changes in changes | group_by(attribute="type") -%}

##### {{ type | typeheader }}

{% for change in changes -%}
- **{{ change.description }}** ([`{{ change.commit.short_id }}`])

{% if change.body -%}
{{ change.body | indent(n=2) }}

{% endif -%}
{%- endfor -%}

{% endfor %}
{% endfor %}
{%- endfor -%}
)
-->
