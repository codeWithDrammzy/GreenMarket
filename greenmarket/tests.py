{% for order in orders %}
  <div class="border p-4 rounded">
    <p>Order ID: {{ order.id }}</p>
    <p>Status: {{ order.get_status_display }}</p>
    
    {% if order.status == "approved" %}
      <a href="{% url 'start-payment' order.id %}" class="btn btn-success">Proceed to Payment</a>
    {% elif order.status == "rejected" %}
      <p class="text-red-600">Rejected: {{ order.rejection_reason }}</p>
    {% else %}
      <p class="text-gray-500">Pending Approval...</p>
    {% endif %}
  </div>
{% endfor %}
