(function(){
  function init(){
    // action cards: click to show section and fetch data
    document.querySelectorAll('.action-card[data-action]').forEach(el=>{
      el.addEventListener('click', ()=>{
        const action = el.dataset.action;
        if(action === 'grading') show('grading');
        if(action === 'classes') show('classes');
        if(action === 'inc') show('inc');
      });
    });
    // when show occurs, modules will fetch as needed via show listeners below
    function show(id){ document.querySelectorAll('.content-section').forEach(c=>c.classList.add('hidden')); const target = document.getElementById(id); if(target) target.classList.remove('hidden');
      // trigger module fetches
      if(id === 'grading' && window.FacultyGrading) window.FacultyGrading.loadClasses();
      if(id === 'classes' && window.FacultyClasses) window.FacultyClasses.fetchClasses();
      if(id === 'inc' && window.FacultyInc) window.FacultyInc.fetchInc();
    }
  }
  document.addEventListener('DOMContentLoaded', init);
})();
