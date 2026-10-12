(function(){'use strict';document.documentElement.classList.add('js');
var btn=document.getElementById('menu-btn'),nav=document.getElementById('site-nav');
if(btn&&nav){btn.addEventListener('click',function(){var open=nav.classList.toggle('open');btn.setAttribute('aria-expanded',open?'true':'false');});document.addEventListener('keydown',function(e){if(e.key==='Escape'&&nav.classList.contains('open')){nav.classList.remove('open');btn.setAttribute('aria-expanded','false');btn.focus();}});}
var input=document.getElementById('guide-filter'),out=document.getElementById('filter-count');
if(input){var root=input.closest('section')||document, cards=Array.prototype.slice.call(root.querySelectorAll('[data-guide]'));
if(!cards.length){cards=Array.prototype.slice.call(document.querySelectorAll('.grid .card'));cards.forEach(function(c){c.setAttribute('data-guide',(c.innerText||c.textContent||'').toLowerCase());});}
var empty=document.getElementById('guide-empty');if(!empty){empty=document.createElement('p');empty.id='guide-empty';empty.className='empty-state';empty.setAttribute('role','status');empty.textContent='No guides match that search. Try “tractor”, “trolley”, “APK” or “controls”.';empty.hidden=true;var parent=cards.length?cards[cards.length-1].parentNode:null;if(parent)parent.insertAdjacentElement('afterend',empty);}
function filter(){var q=input.value.trim().toLowerCase(),n=0;cards.forEach(function(c){var hay=(c.getAttribute('data-guide')||c.innerText||c.textContent||'').toLowerCase();var show=!q||hay.indexOf(q)!==-1;c.hidden=!show;if(show)n++;});if(out)out.textContent=q?n+' of '+cards.length+' guides match':cards.length+' guides';if(empty)empty.hidden=!q||n>0;}
input.addEventListener('input',filter);filter();}
})();