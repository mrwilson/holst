{% if nat %}
*nat
:PREROUTING ACCEPT
:POSTROUTING ACCEPT
:OUTPUT ACCEPT

COMMIT

{% endif %}
*filter
:INPUT DROP
:FORWARD DROP
:OUTPUT DROP

{% for chain in chains %}
:{{ chain }} - 
{% endfor %}

{% if loopback %}
-A OUTPUT -o lo -j ACCEPT
-A INPUT -i lo -j ACCEPT
{% endif %}

{% if accept_established %}
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
-A OUTPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
{% endif %}

{% for rule in incoming_rules %}
-A INPUT -p {{ rule.protocol }} -m multiport --dports {{ rule.ports }} -m state --state NEW -j {{ rule.name }} 
{% endfor %}

{% for rule in outgoing_rules %}
-A OUTPUT -p {{ rule.protocol }} -m multiport --dports {{ rule.ports }} -m state --state NEW -j {{ rule.name }}
{% endfor %}

{% for rule in incoming_rules %}
  {% if rule.source %}
    {% for ip in rule.source %}
-A {{ rule.name }} --source {{ ip }} -j {{ rule.operation }} 
    {% endfor %}
  {% else %}
-A {{ rule.name }} -j {{ rule.operation }}
  {% endif %}
{% endfor %}

{% for rule in outgoing_rules %}
  {% if rule.source %}
    {% for ip in rule.source %}
-A {{ rule.name }} --source {{ ip }} -j {{ rule.operation }}
    {% endfor %}
  {% else %}
-A {{ rule.name }} -j {{ rule.operation }}
  {% endif %}
{% endfor %}

COMMIT
