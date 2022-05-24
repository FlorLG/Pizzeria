var ejemplo_vModel = new Vue({
    el: '#pedidos',
    data: {
      titulo: "Pedido a la Pizzería Firenze",
      pizzas: [
        // Objetos dentro del array frutas con el par clave-valor
        { nombre: "Promo: Muzza Grande + 2 empanadas + Gaseosa 2 L", cantidad: 0 },
        { nombre: "Grande de Muzarella", cantidad: 0 },
        { nombre: "Grande Napolitana", cantidad: 0 },
        { nombre: "Docena de empanadas surtidas", cantidad: 0 },
        { nombre: "Coca Cola de 2 litros", cantidad: 0 },
        { nombre: "Quilmes de 1 litro", cantidad: 0 },
        { nombre: "Brownie con helado", cantidad: 0 },
      ],
      nuevaPizza: '',
      total: 0      
    },
    methods: {
      agregarPizzaConIF() {
        if (this.nuevaPizza != "") {
          this.pizzas.push({ nombre: this.nuevaPizza, cantidad: 1 });
          this.nuevaPizza = '';
        }
      }
    },
    saboresPizzas(){   //no lo usé al final
      for (pizza of this.pizzas) {
        var sabores = {sabor:this.sabor, cant:this.cant}
        this.pizzas.push(sabores);
        this.sabor = "";
        this.cant = "";
       }
    },
    getInputName(index, dataName){  //para imprimir dinámicamente los sabores de las pizzas con sus cantidades
      return "pizza["+index+"]["+dataName+"]";
    },
    computed: {
      sumarPizzas() {//Muestra sumatoria total de cantidades de frutas.
        this.total = 0;
        for (pizza of this.pizzas) {
          this.total += pizza.cantidad; //acumulador
        }
        return this.total;
      }

     
    }
  })