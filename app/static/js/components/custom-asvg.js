(function() {
    class CustomASVG extends HTMLElement {
      // set which attributes changes will trigger the attributeChangedCallback
      static get observedAttributes() {
        return ["text", "ref", "svg"];
      }
  
      // part of custom element lifecylce hooks: set property defaults, make root element a shadow root and set up event listeners in constructor
      // call render here to render elements that do not have any custom observed attributes
      constructor() {
        super();
        this.text = "Opcion";
        this.ref = "main";
        this.svg = `
        <svg viewBox="0 0 22 22" xmlns="http://www.w3.org/2000/svg">
            <g fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19.96 6.65v8.15c0 3.02-1.89 5.15-4.91 5.15H6.4c-3.02 0-4.9-2.13-4.9-5.15V6.65c0-3.02 1.89-5.15 4.9-5.15h8.65c3.02 0 4.91 2.13 4.91 5.15z"></path>
            <path d="M4.031 15.182l1.53-1.613a1.405 1.405 0 012.031-.008l.885.903c.597.61 1.59.565 2.131-.094l2.23-2.71a1.687 1.687 0 012.514-.105l2.076 2.142M9.063 7.884a1.754 1.754 0 11-3.506 0 1.754 1.754 0 013.506 0z"></path>
            </g>
        </svg>
        `;
        this.attachShadow({ mode: "open" });
        this.onclick = this.onClick;
      }
  
      // part of custom element lifecylce hooks: userful for running setup code such as fetching resources or rendering
      connectedCallback() {
        this.render();
      }
  
      // new render method to set styles and html elments to be displayed inside the shodow DOM
      render() {
        this.shadowRoot.innerHTML = `
        <style>
        :host{
          flex: 1 0 21%;
          background-color: var(--container-color);
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          text-align: center;
          width: 140px;
          height: 140px;
          border-radius: 10px;
          border: 0.1rem solid var(--border-color);
          transition: border-color ease-in-out 0.15s, box-shadow ease-in-out 0.15s, -webkit-box-shadow ease-in-out 0.15s;
          cursor: pointer;
          position: relative;
          user-select: none;
          appearance: none;
        }
        .label{
          height:30px;
          font-size:1rem;
          font-width:bold;
          color:var(--text-color)
        }
        .check{
          position:absolute;
          top:5px;
          right:2px;
          fill: var(--body-color);
        }
        svg:nth-child(odd){
          width: 60px !important;
          height: 60px !important;
          fill:var(--icon-color) !important;;
        }
        :host(:hover),
        :host(:active) {
          border-color: var(--primary);
          color: var(--primary);
        }
        :host(:hover) > svg,
        :host(:active) > svg{
          fill:var(--primary) !important;
        }
        @media only screen and (max-width: 600px) {
          :host{
            flex: 1 0 41%;
          }
        }
        </style>

        <svg class="check" xmlns="http://www.w3.org/2000/svg" width="24" height="24"><path d="M16 2H8C4.691 2 2 4.691 2 8v13a1 1 0 0 0 1 1h13c3.309 0 6-2.691 6-6V8c0-3.309-2.691-6-6-6zm-5 14.414-3.707-3.707 1.414-1.414L11 13.586l4.793-4.793 1.414 1.414L11 16.414z"></path></svg>
        ${this.svg}
        <label class="label">${this.text}</label>
      `;
      }

    // new onClick method to change the attributes of the custom elements
    onClick() {
      location.href=this.ref;
    }
  
      // part of custom element lifecylce hooks: this method will run whenever an attributes listed in observedAttributes changes
      attributeChangedCallback(name, oldValue, newValue) {
        this.getAttribute("text")
          ? (this.text = this.getAttribute("text"))
          : null;
        this.getAttribute("ref")
          ? (this.ref = this.getAttribute("ref"))
          : null;
        this.getAttribute("svg")
          ? (this.svg = this.getAttribute("svg"))
          : null;
        this.render();
}}
  customElements.define("custom-asvg", CustomASVG);
})();
  