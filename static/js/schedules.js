(function(){
  function init(){ document.addEventListener('click', function(e){ if(e.target.matches('.btn-edit-schedule')) handleEditSchedule(e); }); }
  function fetchSchedules(){ return fetch('/api/schedules').then(r=>r.json()).then(renderSchedules).catch(e=>console.error(e)); }
  function renderSchedules(list){ const ul = document.querySelector('.schedule-list'); if(!ul) return; ul.innerHTML = ''; list.forEach(s=>{ const li = document.createElement('li'); li.dataset.schedId = s.id; li.innerHTML = `${s.title} - ${s.times} <button class="btn-edit-schedule btn">Edit</button>`; ul.appendChild(li); }); }
  function handleEditSchedule(e){ const li = e.target.closest('li'); const id = li ? li.dataset.schedId : null; if(!id) return alert('Schedule ID missing'); const newTitle = prompt('Edit schedule title:', li.textContent.trim()); if(newTitle === null) return; fetch(`/api/schedules/${id}`, { method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify({title:newTitle})}).then(r=>r.json()).then(d=>{ alert(d.message||'Updated (stub)'); fetchSchedules(); }).catch(e=>{ console.error(e); alert('Failed to update schedule.'); }); }
  window.Schedules = { init, fetchSchedules };
  document.addEventListener('DOMContentLoaded', init);
})();