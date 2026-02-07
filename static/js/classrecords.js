(function(){
  function init(){ document.addEventListener('click', function(e){ if(e.target.matches('.btn-view-class')) handleViewClass(e); }); }
  function fetchClassRecords(){ return fetch('/api/classrecords').then(r=>r.json()).then(renderClassRecords).catch(e=>console.error(e)); }
  function renderClassRecords(list){ const tbody = document.querySelector('.classrecords-table tbody'); if(!tbody) return; tbody.innerHTML = ''; list.forEach(c=>{ const tr = document.createElement('tr'); tr.dataset.classId = c.id; tr.innerHTML = `<td>${c.course}</td><td>${c.instructor}</td><td>${c.term}</td><td><button class="btn-view-class btn">View</button></td>`; tbody.appendChild(tr); }); }
  function handleViewClass(e){ const tr = e.target.closest('tr'); const id = tr ? tr.dataset.classId : null; if(!id) return alert('Class ID missing'); fetch(`/api/classrecords/${id}`).then(r=>r.json()).then(d=>{ alert(`Class Record for ${d.course}\nInstructor: ${d.instructor}\nStudents: ${d.students ? d.students.length : 0}`); }).catch(e=>{ console.error(e); alert('Failed to fetch class record.'); }); }
  window.ClassRecords = { init, fetchClassRecords };
  document.addEventListener('DOMContentLoaded', init);
})();
