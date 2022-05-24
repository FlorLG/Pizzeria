const shop = [
    {
      name: "Grande de Muzzarella",
      price: 790,
      quantity: 0
    },
    {
      name: "Chica de Muzzarella",
      price: 590,
      quantity: 0
    },
    {
      name: "Grande Napolitana",
      price: 890,
      quantity: 0
    },
    {
      name: "Chica Napolitana",
      price: 650,
      quantity: 0
    },
    {
      name: "Docena de empanadas surtidas",
      price: 1200,
      quantity: 0
    }
  ];
  
  const vm = new Vue({
    el: "#app",
    data: {
      items: [],
      shop: shop,
      showCart: false,
      verified: false,
      quantity: 1
    },
    computed: {
      total() {
        var total = 0;
        for(var i = 0; i < this.items.length; i++) {
          total += this.items[i].price;
        }
        return total;
      }
    },
    methods: {
      addToCart(item) {
        item.quantity += 1;
        this.items.push(item);
      },
      removeFromCart(item) {
        item.quantity -= 1;
        this.items.splice(this.items.indexOf(item), 1);
      }
    }
  });