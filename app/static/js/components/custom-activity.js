(function() {
    class CustomActivity extends HTMLElement {  
       // set which attributes changes will trigger the attributeChangedCallback
       static get observedAttributes() {
        return ["index", "codigo", "estado", "inicio", "fin", "empresa", "documento", "nombre"];
      }
      // part of custom element lifecylce hooks: set property defaults, make root element a shadow root and set up event listeners in constructor
      // call render here to render elements that do not have any custom observed attributes
      constructor() {
        super();
        this.index = 1;
        this.codigo= "72539751";
        this.estado= "ATENDIDO";
        this.inicio= "10/20/2021";
        this.fin= "-";
        this.empresa= "INSTITUTO DE ESPECAILIDADES";
        this.documento= "72539751";
        this.nombre= "PATRICK ALONSO";

        this.attachShadow({ mode: "open" });
      }
  
      // part of custom element lifecylce hooks: userful for running setup code such as fetching resources or rendering
      connectedCallback() {
        this.render();
      }
  
      // new render method to set styles and html elments to be displayed inside the shodow DOM
      render() {
        this.shadowRoot.innerHTML = `
        <style>
          @import url("localhost:5000/grid.css")
        </style>
        <style>
        :host{
          width:300px;
          padding: .35rem;
        }
        .header,
        .body,
        .footer{
          padding: .35rem .8rem;
          margin-bottom: .35rem;
        }
        .header{
          border-radius: var(--border-radius);
          display: flex;
          gap: .5rem;
          justify-content: space-between;
          align-items: center;
          background-color: var(--container-ascent-color);
        }
        .dot{
          height: 25px;
          width: 25px;
          background-color: var(--body-ascent-color);
          border-radius: 50%;
          display: inline-block;
          text-align:center;
          font-size:1rem;
        }
        .title{
          padding:.3rem;
          border: solid 2px var(--border-color);
          font-weight:bold;
        }
        .state{
          color:var(--red);
          font-size: .7rem;
          text-transform: lowercase;
        }
        .body{
          border-radius: var(--border-radius);
          background-color:var(--container-color);
          text-align:center;
        }
        .text{
          border: solid 1px var(--border-color);
        }
        .text-ascent{
          text-align:center;
          color:var(--purple);
        }
        .footer{
          border-radius: var(--border-radius);
          background-color:var(--container-ascent-color);
          text-align:end;
          text-align: -moz-right;
        }
        .btn {
          overflow: visible;
          margin: 0;
          padding: 0;
          border: 0;
          background: transparent;
          font: inherit;
          line-height: normal;
          cursor: pointer;
          -moz-user-select: text;
          display: flex;
              align-items: center;
              justify-content: center;
          text-decoration: none;
          text-transform: uppercase;
          padding: .2rem .7rem;
          background-color: #fff;
          color: #666;
          border: 2px solid #666;
          border-radius: 6px;
          margin-bottom: .2rem;
          transition: all 0.5s ease;
        }
        </style>

        <div class="header">
          <div class="dot">${this.index}</div>
          <label class="title">${this.codigo}</label>
          <label class="state">${this.estado}</label>
        </div>
        <div class="body">
          <div>
            <div class="text">${this.documento}</div>
            <div class="text">${this.nombre}</div>
          </div>
          <label class="text-ascent">${this.empresa}</label>
        </div>
        <div class="footer">
        <button class="btn" onClick="f_onClick(${this.index});return false;">
          Ver Detalle
        </button>
        </div>
      `;
      }
      // part of custom element lifecylce hooks: this method will run whenever an attributes listed in observedAttributes changes
      attributeChangedCallback(name, oldValue, newValue) {
        this.getAttribute("index")
          ? (this.index = this.getAttribute("index"))
          : null;
        this.getAttribute("codigo")
          ? (this.codigo = this.getAttribute("codigo"))
          : null;
        this.getAttribute("estado")
          ? (this.estado = this.getAttribute("estado"))
          : null;
        this.getAttribute("inicio")
          ? (this.inicio = this.getAttribute("inicio"))
          : null;
        this.getAttribute("fin")
          ? (this.fin = this.getAttribute("fin"))
          : null;
        this.getAttribute("empresa")
          ? (this.empresa = this.getAttribute("empresa"))
          : null;
        this.getAttribute("documento")
          ? (this.documento = this.getAttribute("documento"))
          : null;
        this.getAttribute("nombre")
          ? (this.nombre = this.getAttribute("nombre"))
          : null;
        this.render();
}}
  customElements.define("custom-activity", CustomActivity);
})();
  