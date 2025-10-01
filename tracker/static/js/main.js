    document.addEventListener('DOMContentLoaded', function () {
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: '/tasks/api/events/',  // Django endpoint that returns tasks as JSON
        });
        calendar.render();
    });