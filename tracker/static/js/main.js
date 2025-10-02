    document.addEventListener('DOMContentLoaded', function () {
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: '/tasks/api/events/',  // Django endpoint that returns tasks as JSON
        });
        calendar.render();
    });


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

function updateTask(id, status, order) {
  fetch("{% url 'update_task_status' %}", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({ id: id, status: status, order: order })
  }).then(r=>r.json()).then(data=>{
    console.log("Updated:", data);
  });
}

document.querySelectorAll('.status-select').forEach(sel=>{
  sel.addEventListener('change', ()=>{
    const id = sel.dataset.id;
    const status = sel.value;
    const order = document.querySelector(`.order-input[data-id="${id}"]`).value;
    updateTask(id, status, order);
  });
});

document.querySelectorAll('.order-input').forEach(inp=>{
  inp.addEventListener('change', ()=>{
    const id = inp.dataset.id;
    const order = inp.value;
    const status = document.querySelector(`.status-select[data-id="${id}"]`).value;
    updateTask(id, status, order);
  });
});


const toggleBtn = document.getElementById("theme-toggle");
const body = document.body;

// Load saved theme
if (localStorage.getItem("theme") === "dark") {
  body.classList.add("dark-mode");
  toggleBtn.textContent = "☀️ Light Mode";
}

toggleBtn.addEventListener("click", () => {
  body.classList.toggle("dark-mode");

  if (body.classList.contains("dark-mode")) {
    toggleBtn.textContent = "☀️ Light Mode";
    localStorage.setItem("theme", "dark");
  } else {
    toggleBtn.textContent = "🌙 Dark Mode";
    localStorage.setItem("theme", "light");
  }
});


if (!localStorage.getItem("theme")) {
  if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    body.classList.add("dark-mode");
    toggleBtn.textContent = "☀️ Light Mode";
  }
}