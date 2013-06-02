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
:OUTPUT ACCEPT

{% for chain in chains %}
:{{ chain }} - 
{% endfor %}
{% for rule in rules %}
-A INPUT -p {{ rule.protocol }} -m {{ rule.module }} {{ rule.ports }} -m state --state NEW -j {{ rule.name }} 
{% endfor %}
