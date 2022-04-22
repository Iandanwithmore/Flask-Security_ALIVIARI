const template = document.createElement('template');
template.innerHTML = `
    <style>
        .tooltip-container{
            display:inline-block;
            position:relative;
            z-index:10;
        }
        .alert{
            fill:var(--yellow);
        }
        .cancel{
            fill:var(--red);
            display:none;
        }
        .svg{
            width:1em;
            cursor:pointer;
        }
        .text-container{
            position: absolute;
            bottom:125%;
            z-index:9;
            width: 300px;
            background: var(--container-color);
            box-shadow: 5px 5px 10px rgba(0,0,0,.1);
            font-size: .8em;
            border-radius: .5em;
            padding: 1em;
            transform: scale(0);
            transform-origin: bottom left;
            transition: transform .5s cubiec-bezier(0.860, 0.000, 0.070,1);
        }
    </style>

    <div class="tooltip-container">
        <svg class="alert" width="24" height="24" viewBox="0 0 24 24">
            <path d="M16 2H8C4.691 2 2 4.691 2 8v13a1 1 0 0 0 1 1h13c3.309 0 6-2.691 6-6V8c0-3.309-2.691-6-6-6zm4 14c0 2.206-1.794 4-4 4H4V8c0-2.206 1.794-4 4-4h8c2.206 0 4 1.794 4 4v8z"></path><path d="M11 6h2v8h-2zm0 10h2v2h-2z"></path>
        </svg>
        <svg class="cancel" width="24" height="24" viewBox="0 0 24 24">
            <path d="M16 2H8C4.691 2 2 4.691 2 8v13a1 1 0 0 0 1 1h13c3.309 0 6-2.691 6-6V8c0-3.309-2.691-6-6-6zm4 14c0 2.206-1.794 4-4 4H4V8c0-2.206 1.794-4 4-4h8c2.206 0 4 1.794 4 4v8z"></path><path d="M15.292 7.295 12 10.587 8.708 7.295 7.294 8.709l3.292 3.292-3.292 3.292 1.414 1.414L12 13.415l3.292 3.292 1.414-1.414-3.292-3.292 3.292-3.292z"></path>
        </svg>
        <div class="text-container">
            <slot name="msg" />
        </div>
    </div>
`;

class Popup extends HTMLElement{
    constructor(){
        super();
        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));
    }

    tooltip(expandState){
        const tooltip = this.shadowRoot.querySelector('.text-container');
        const alert =  this.shadowRoot.querySelector('.alert');
        const cancel =  this.shadowRoot.querySelector('.cancel');

        if(expandState == true){
            tooltip.style.transform = 'scale(1)';
            alert.style.display = 'none';
            cancel.style.display = 'block';
            expandState = false;
        }else{
            tooltip.style.transform = 'scale(0)';
            alert.style.display = 'block';
            cancel.style.display = 'none';
        }
    }

    connectedCallback() {
        this.shadowRoot.querySelector('.alert').addEventListener('click', () =>{
            this.tooltip(true);
        })
        this.shadowRoot.querySelector('.cancel').addEventListener('click', () =>{
            this.tooltip(false);
        })
      }
}

window.customElements.define('custom-popup', Popup)