/* MicroDatepicker - lightweight date picker (ES-only) - MIT License */
(function(){
  const pad=(n)=> (n<10?'0':'')+n;
  const months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
  const days = ['Lu','Ma','Mi','Ju','Vi','Sa','Do'];

  function parseDMY(str){
    if(!str) return null;
    const m = String(str).match(/^(\d{1,2})[\/](\d{1,2})[\/](\d{4})$/);
    if(!m) return null;
    const d = new Date(Number(m[3]), Number(m[2])-1, Number(m[1]));
    return isNaN(d.getTime())? null : d;
  }

  function formatDMY(d){ return pad(d.getDate())+'/'+pad(d.getMonth()+1)+'/'+d.getFullYear(); }

  class Picker{
    constructor(input){
      this.input = input;
      this.visible = false;
      this.date = parseDMY(input.value) || new Date();
      this.month = this.date.getMonth();
      this.year = this.date.getFullYear();
      this._build();
      this._bind();
    }
    _build(){
      const root = document.createElement('div');
      root.className = 'mdp-root hidden';
      root.setAttribute('role','dialog');
      root.innerHTML = `
        <div class="mdp-head">
          <button type="button" class="mdp-nav mdp-prev" aria-label="Anterior">‹</button>
          <div class="mdp-title"></div>
          <button type="button" class="mdp-nav mdp-next" aria-label="Siguiente">›</button>
        </div>
        <div class="mdp-grid">
          <div class="mdp-days"></div>
          <div class="mdp-dates"></div>
        </div>`;
      // days header
      const daysEl = root.querySelector('.mdp-days');
      days.forEach(d=>{ const e=document.createElement('span'); e.textContent=d; daysEl.appendChild(e); });
      document.body.appendChild(root);
      this.root = root;
      this.title = root.querySelector('.mdp-title');
      this.dates = root.querySelector('.mdp-dates');
      this._render();
    }
    _bind(){
      this.root.querySelector('.mdp-prev').addEventListener('click', ()=>{ this._change(-1); });
      this.root.querySelector('.mdp-next').addEventListener('click', ()=>{ this._change(1); });
      document.addEventListener('click', (e)=>{
        if(!this.visible) return;
        if(e.target===this.input) return;
        if(this.root.contains(e.target)) return;
        this.close();
      });
      document.addEventListener('keydown', (e)=>{ if(this.visible && e.key==='Escape'){ this.close(); } });
    }
    _change(delta){
      this.month += delta;
      if(this.month<0){ this.month=11; this.year--; }
      if(this.month>11){ this.month=0; this.year++; }
      this._render();
    }
    _render(){
      this.title.textContent = months[this.month] + ' ' + this.year;
      const first = new Date(this.year, this.month, 1);
      const startOffset = ( (first.getDay()||7) - 1 ); // Monday=0
      const daysInMonth = new Date(this.year, this.month+1, 0).getDate();
      const frag = document.createDocumentFragment();
      this.dates.innerHTML='';
      for(let i=0;i<startOffset;i++){ const emp=document.createElement('span'); emp.className='mdp-empty'; frag.appendChild(emp); }
      for(let d=1; d<=daysInMonth; d++){
        const btn = document.createElement('button');
        btn.type='button'; btn.className='mdp-date'; btn.textContent = String(d);
        const dt = new Date(this.year, this.month, d);
        if(this.input.value){
          const sel = parseDMY(this.input.value);
          if(sel && sel.getFullYear()===dt.getFullYear() && sel.getMonth()===dt.getMonth() && sel.getDate()===dt.getDate()){
            btn.classList.add('is-selected');
          }
        }
        btn.addEventListener('click', ()=>{
            this.input.value = formatDMY(dt);
            this.input.dispatchEvent(new Event('input', {bubbles:true}));
            this.input.dispatchEvent(new Event('change', {bubbles:true}));
            this.close();
        });
        frag.appendChild(btn);
      }
      this.dates.appendChild(frag);
    }
    open(){
      const rect = this.input.getBoundingClientRect();
      this.root.style.minWidth = Math.max(220, rect.width)+'px';
      this.root.style.left = (window.scrollX + rect.left)+'px';
      this.root.style.top = (window.scrollY + rect.bottom + 6)+'px';
      this.root.classList.remove('hidden');
      this.visible = true;
    }
    close(){ this.root.classList.add('hidden'); this.visible=false; }
  }

  window.MicroDatepicker = {
    attach(input){
      if(input._mdp) return input._mdp;
      const p = new Picker(input);
      input._mdp = p;
      input.addEventListener('focus', ()=>p.open(), {passive:true});
      input.addEventListener('click', ()=>p.open(), {passive:true});
      return p;
    }
  };
})();
