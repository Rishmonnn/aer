(function(){
  // --- Calendar Logic (Ported from Program Head) ---
  let currDate = new Date();
  
  function renderCalendar() {
      const m = currDate.getMonth(), y = currDate.getFullYear();
      const body = document.getElementById("calendar-body");
      if (!body) return;

      const firstDay = new Date(y, m, 1).getDay();
      const lastDate = new Date(y, m + 1, 0).getDate();
      let days = "<tr>";
      for (let i = 0; i < firstDay; i++) days += "<td></td>";

      const today = new Date();
      for (let d = 1; d <= lastDate; d++) {
          if ((d + firstDay - 1) % 7 === 0 && d !== 1) days += "</tr><tr>";
          const isToday = d === today.getDate() && m === today.getMonth() && y === today.getFullYear();
          days += `<td class="${isToday ? 'today' : ''}">${d}</td>`;
      }
      days += "</tr>";
      body.innerHTML = days;
      
      // Update selects if they exist
      const mSelect = document.getElementById('monthSelect');
      const ySelect = document.getElementById('yearSelect');
      if(mSelect) mSelect.value = m;
      if(ySelect) ySelect.value = y;
  }

  // Global functions for inline HTML onclick events
  window.changeMonth = function(step) {
      currDate.setMonth(currDate.getMonth() + step);
      renderCalendar();
  };

  window.updateCalendarFromSelect = function() {
      const yVal = document.getElementById('yearSelect').value;
      const mVal = document.getElementById('monthSelect').value;
      currDate.setFullYear(parseInt(yVal));
      currDate.setMonth(parseInt(mVal));
      renderCalendar();
  };

  // --- Main Init ---
  function init(){
    // Initialize Calendar
    renderCalendar();

    // Event listeners for the NEW Quick Action buttons
    document.querySelectorAll('.action-trigger[data-action]').forEach(el=>{
      el.addEventListener('click', ()=>{
        const action = el.dataset.action;
        showSection(action); // Uses the global showSection from main.js or below
      });
    });

    // Helper: Internal show function if not global
    function showSection(id){ 
        document.querySelectorAll('.content-section').forEach(c=>c.classList.add('hidden')); 
        const target = document.getElementById(id); 
        if(target) target.classList.remove('hidden');
      
        // Trigger module fetches
        if(id === 'grading' && window.FacultyGrading) window.FacultyGrading.loadClasses();
        if(id === 'classes' && window.FacultyClasses) window.FacultyClasses.fetchClasses();
        if(id === 'inc' && window.FacultyInc) window.FacultyInc.fetchInc();
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})();