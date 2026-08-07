// Dynamic Dashboard Controller with Live Chart.js Fetching
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('weeklyActivityChart')) {
    loadDashboardStats();
  }
});

let weeklyChartInstance = null;
let skillChartInstance = null;

async function loadDashboardStats() {
  try {
    const response = await fetch('/api/dashboard/stats');
    const data = await response.json();

    // Update KPI numbers dynamically
    document.getElementById('val-readiness').innerText = data.kpi.career_readiness_score + '%';
    document.getElementById('val-resume').innerText = data.kpi.resume_match_score + '%';
    document.getElementById('val-interview').innerText = data.kpi.interview_score + '/100';
    document.getElementById('val-chats').innerText = data.kpi.total_ai_chats;

    // Render Weekly Activity Bar Chart
    renderWeeklyChart(data.charts.weekly_activity);

    // Render Skill Breakdown Radar Chart
    renderSkillChart(data.charts.skill_match_breakdown);

  } catch (error) {
    console.error("Error fetching dashboard statistics:", error);
  }
}

function renderWeeklyChart(weeklyData) {
  const ctx = document.getElementById('weeklyActivityChart').getContext('2d');
  
  if (weeklyChartInstance) {
    weeklyChartInstance.destroy();
  }

  weeklyChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: weeklyData.labels,
      datasets: [
        {
          label: 'AI Career Queries',
          data: weeklyData.chat_queries,
          backgroundColor: '#06b6d4',
          borderRadius: 6
        },
        {
          label: 'Voice Practice (mins)',
          data: weeklyData.voice_practice_mins,
          backgroundColor: '#8b5cf6',
          borderRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#9ca3af' } }
      },
      scales: {
        x: { ticks: { color: '#9ca3af' }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y: { ticks: { color: '#9ca3af' }, grid: { color: 'rgba(255,255,255,0.05)' } }
      }
    }
  });
}

function renderSkillChart(skillData) {
  const ctx = document.getElementById('skillRadarChart').getContext('2d');
  
  if (skillChartInstance) {
    skillChartInstance.destroy();
  }

  skillChartInstance = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: skillData.labels,
      datasets: [{
        label: 'Skill Proficiency %',
        data: skillData.data,
        backgroundColor: 'rgba(6, 182, 212, 0.2)',
        borderColor: '#06b6d4',
        pointBackgroundColor: '#6366f1'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#9ca3af' } }
      },
      scales: {
        r: {
          grid: { color: 'rgba(255,255,255,0.1)' },
          pointLabels: { color: '#9ca3af' },
          ticks: { backdropColor: 'transparent', color: '#9ca3af' }
        }
      }
    }
  });
}
