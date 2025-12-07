$(document).ready(function () {
  // Click handler for link previews
  $('.link-preview').on('click', function(e) {
    if (!e.target.closest('.open-btn') && !e.target.closest('.fullscreen-btn')) {
      const linkContainer = $(this).closest('.web-link');
      if (linkContainer.attr('id') === 'incoisLink') {
        openExternal('https://incois.gov.in/OON/index.jsp');
      } else if (linkContainer.attr('id') === 'zoomEarthLink') {
        openExternal('https://zoom.earth/maps/satellite/');
      }
    }
  });

  eel.init()
  $(".text").textillate({
    loop: true,
    speed: 1500,
    sync: true,
    in: {
      effect: "bounceIn",
    },
    out: {
      effect: "bounceOut",
    },
  });

  $(".siri-message").textillate({
    loop: true,
    sync: true,
    in: {
      effect: "fadeInUp",
      sync: true,
    },
    out: {
      effect: "fadeOutUp",
      sync: true,
    },
  });

  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 940,
    style: "ios9",
    amplitude: "1",
    speed: "0.30",
    height: 200,
    autostart: true,
    waveColor: "#ff0000",
    waveOffset: 0,
    rippleEffect: true,
    rippleColor: "#ffffff",
  });

  $("#MicBtn").click(function () {
    eel.play_assistant_sound();
    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);

    eel.takeAllCommands();
  });

  function doc_keyUp(e) {
    // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

    if (e.key === "j" && e.metaKey) {
      eel.play_assistant_sound();
      $("#Oval").attr("hidden", true);
      $("#SiriWave").attr("hidden", false);
      eel.takeAllCommands();
    }
  }
  document.addEventListener("keyup", doc_keyUp, false);

  function PlayAssistant(message) {
    if (message != "") {
      $("#Oval").attr("hidden", true);
      $("#SiriWave").attr("hidden", false);
      eel.takeAllCommands(message);
      $("#chatbox").val("");
      $("#MicBtn").attr("hidden", false);
      $("#SendBtn").attr("hidden", true);
    } else {
      console.log("Empty message, nothing sent."); // Log if the message is empty
    }
  }

  function ShowHideButton(message) {
    if (message.length == 0) {
      $("#MicBtn").attr("hidden", false);
      $("#SendBtn").attr("hidden", true);
    } else {
      $("#MicBtn").attr("hidden", true);
      $("#SendBtn").attr("hidden", false);
    }
  }

  $("#chatbox").keyup(function () {
    let message = $("#chatbox").val();
    console.log("Current chatbox input: ", message); // Log input value for debugging
    ShowHideButton(message);
  });

  $("#SendBtn").click(function () {
    let message = $("#chatbox").val();
    PlayAssistant(message);
  });

  $("#chatbox").keypress(function (e) {
    key = e.which;
    if (key == 13) {
      let message = $("#chatbox").val();
      PlayAssistant(message);
    }
  });
});

// Global variable to store current URL
let currentUrl = '';

// Open external link in new window
function openExternal(url) {
  window.open(url, '_blank', 'noopener,noreferrer');
}

// Fullscreen functionality with iframe fallback
function openFullscreen(url, title) {
  currentUrl = url;
  const modal = document.getElementById('fullscreenModal');
  const iframe = document.getElementById('fullscreenIframe');
  const titleElement = document.getElementById('fullscreenTitle');
  const externalMessage = document.getElementById('externalLinkMessage');
  
  titleElement.textContent = title;
  modal.style.display = 'flex';
  
  // Show external link message directly for these blocked sites
  iframe.style.display = 'none';
  externalMessage.style.display = 'flex';
  
  // Hide main content
  document.querySelector('.container').style.display = 'none';
}

// Open current URL in new window from fullscreen
function openInNewWindow() {
  if (currentUrl) {
    window.open(currentUrl, '_blank', 'noopener,noreferrer');
    closeFullscreen();
  }
}

function closeFullscreen() {
  const modal = document.getElementById('fullscreenModal');
  const iframe = document.getElementById('fullscreenIframe');
  const externalMessage = document.getElementById('externalLinkMessage');
  
  modal.style.display = 'none';
  iframe.src = '';
  iframe.style.display = 'none';
  externalMessage.style.display = 'none';
  currentUrl = '';
  
  // Show main content
  document.querySelector('.container').style.display = 'block';
}

// Handle escape key to close fullscreen
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    const modal = document.getElementById('fullscreenModal');
    if (modal.style.display === 'flex') {
      closeFullscreen();
    }
  }
});

// Add click handlers for web links
$(document).ready(function() {
  // Make web links draggable (optional enhancement)
  $('.web-link').on('mousedown', function(e) {
    if (e.target.tagName !== 'IFRAME' && !e.target.closest('.fullscreen-btn')) {
      let isDragging = false;
      let startX = e.clientX;
      let startY = e.clientY;
      let startLeft = parseInt($(this).css('right'));
      let startTop = parseInt($(this).css('top'));
      
      $(document).on('mousemove', function(e) {
        if (!isDragging) {
          isDragging = true;
        }
        
        let newRight = startLeft + (startX - e.clientX);
        let newTop = startTop + (e.clientY - startY);
        
        // Keep within bounds
        newRight = Math.max(0, Math.min(newRight, window.innerWidth - 400));
        newTop = Math.max(0, Math.min(newTop, window.innerHeight - 300));
        
        $(this).css({
          'right': newRight + 'px',
          'top': newTop + 'px'
        });
      }.bind(this));
      
      $(document).on('mouseup', function() {
        $(document).off('mousemove mouseup');
      });
    }
  });
});
