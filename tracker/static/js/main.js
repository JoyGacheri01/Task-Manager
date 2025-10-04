document.addEventListener('DOMContentLoaded', function() {
      var calendarEl = document.getElementById('calendar');
      var calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth',
          headerToolbar: {
              left: 'prev,next today',
              center: 'title',
              right: 'dayGridMonth,timeGridWeek,timeGridDay'
          },
          events: [
              // Add your task events here
          ]
      });
      calendar.render();

      // Update task counts
      updateTaskCounts();

      // Setup drag and drop
      setupDragAndDrop();
  });

  function updateTaskCounts() {
      const pending = document.querySelectorAll('#pending-list .task-item').length;
      const progress = document.querySelectorAll('#progress-list .task-item').length;
      const completed = document.querySelectorAll('#completed-list .task-item').length;

      document.getElementById('pending-count').textContent = pending;
      document.getElementById('progress-count').textContent = progress;
      document.getElementById('completed-count').textContent = completed;

      document.querySelectorAll('.pending-column .task-count')[0].textContent = pending;
      document.querySelectorAll('.progress-column .task-count')[0].textContent = progress;
      document.querySelectorAll('.completed-column .task-count')[0].textContent = completed;
  }

  function setupDragAndDrop() {
      const taskItems = document.querySelectorAll('.task-item');
      const taskLists = document.querySelectorAll('.task-list');

      taskItems.forEach(item => {
          item.addEventListener('dragstart', handleDragStart);
          item.addEventListener('dragend', handleDragEnd);
      });

      taskLists.forEach(list => {
          list.addEventListener('dragover', handleDragOver);
          list.addEventListener('drop', handleDrop);
      });
  }

  let draggedElement = null;

  function handleDragStart(e) {
      draggedElement = this;
      this.classList.add('dragging');
      e.dataTransfer.effectAllowed = 'move';
  }

  function handleDragEnd(e) {
      this.classList.remove('dragging');
  }

  function handleDragOver(e) {
      if (e.preventDefault) {
          e.preventDefault();
      }
      e.dataTransfer.dropEffect = 'move';
      return false;
  }

  function handleDrop(e) {
      if (e.stopPropagation) {
          e.stopPropagation();
      }

      if (draggedElement !== this && this.classList.contains('task-list')) {
          this.appendChild(draggedElement);
          
          // Update task status via AJAX
          const taskId = draggedElement.dataset.id;
          const newStatus = this.dataset.status;
          updateTaskStatus(taskId, newStatus);
          
          updateTaskCounts();
      }

      return false;
  }

  function updateTaskStatus(taskId, status) {
      fetch(`/tasks/${taskId}/update-status/`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify({ status: status })
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              showNotification('Task status updated!', 'success');
          }
      })
      .catch(error => {
          console.error('Error:', error);
          showNotification('Failed to update task', 'error');
      });
  }

  function updateOrder(taskId, order) {
      fetch(`/tasks/${taskId}/update-order/`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify({ order: order })
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              showNotification('Order updated!', 'success');
          }
      })
      .catch(error => {
          console.error('Error:', error);
      });
  }

  function editTask(taskId) {
      // Implement edit functionality
      const taskElement = document.querySelector(`[data-id="${taskId}"]`);
      const title = taskElement.querySelector('.task-title').textContent;
      const newTitle = prompt('Edit task:', title);
      
      if (newTitle && newTitle !== title) {
          fetch(`/tasks/${taskId}/update/`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie('csrftoken')
              },
              body: JSON.stringify({ title: newTitle })
          })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  taskElement.querySelector('.task-title').textContent = newTitle;
                  showNotification('Task updated!', 'success');
              }
          })
          .catch(error => {
              console.error('Error:', error);
              showNotification('Failed to update task', 'error');
          });
      }
  }

  function deleteTask(taskId) {
      if (confirm('Are you sure you want to delete this task?')) {
          fetch(`/tasks/${taskId}/delete/`, {
              method: 'DELETE',
              headers: {
                  'X-CSRFToken': getCookie('csrftoken')
              }
          })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  const taskElement = document.querySelector(`[data-id="${taskId}"]`);
                  taskElement.style.animation = 'fadeOut 0.3s ease-out';
                  setTimeout(() => {
                      taskElement.remove();
                      updateTaskCounts();
                      showNotification('Task deleted!', 'success');
                  }, 300);
              }
          })
          .catch(error => {
              console.error('Error:', error);
              showNotification('Failed to delete task', 'error');
          });
      }
  }

  // Notification system
  function showNotification(message, type) {
      const notification = document.createElement('div');
      notification.className = `notification notification-${type}`;
      notification.textContent = message;
      notification.style.cssText = `
          position: fixed;
          top: 100px;
          right: 20px;
          padding: 1rem 1.5rem;
          background: ${type === 'success' ? '#10b981' : '#ef4444'};
          color: white;
          border-radius: 0.75rem;
          box-shadow: 0 4px 12px rgba(0,0,0,0.2);
          z-index: 10000;
          animation: slideInRight 0.3s ease-out;
      `;
      document.body.appendChild(notification);
      
      setTimeout(() => {
          notification.style.animation = 'slideOutRight 0.3s ease-out';
          setTimeout(() => notification.remove(), 300);
      }, 3000);
  }

  // Helper function to get CSRF token
  function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

  // Add animation keyframes
  const style = document.createElement('style');
  style.textContent = `
      @keyframes fadeOut {
          from { opacity: 1; transform: translateX(0); }
          to { opacity: 0; transform: translateX(20px); }
      }
      @keyframes slideInRight {
          from { opacity: 0; transform: translateX(100px); }
          to { opacity: 1; transform: translateX(0); }
      }
      @keyframes slideOutRight {
          from { opacity: 1; transform: translateX(0); }
          to { opacity: 0; transform: translateX(100px); }
      }

      
  `;
  document.head.appendChild(style);

  // Keyboard shortcuts
  document.addEventListener('keydown', function(e) {
      // Ctrl/Cmd + K to open sidebar
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
          e.preventDefault();
          toggleSidebar();
      }
      // Escape to close sidebar
      if (e.key === 'Escape') {
          const sidebar = document.getElementById('sidebar');
          if (sidebar.classList.contains('open')) {
              toggleSidebar();
          }
      }
  });

  // Auto-save feature for order inputs
  let orderTimeout;
  document.querySelectorAll('.order-input').forEach(input => {
      input.addEventListener('input', function() {
          clearTimeout(orderTimeout);
          const taskId = this.closest('.task-item').dataset.id;
          const value = this.value;
          
          orderTimeout = setTimeout(() => {
              updateOrder(taskId, value);
          }, 1000); // Save after 1 second of no typing
      });
  });