$(document).ready(function() {
    var remainingTime = "{{ remaining_time  }}";
    var countdownElement = $('#countdown');
    
    setInterval(function() {
        var remainingSeconds = parseInt(remainingTime);
        var hours = Math.floor(remainingSeconds / 3600);
        var minutes = Math.floor((remainingSeconds - (hours * 3600)) / 60);
        var seconds = remainingSeconds - (hours * 3600) - (minutes * 60);
        
        var countdownString = hours.toString().padStart(2, '0') + ':' + minutes.toString().padStart(2, '0') + ':' + seconds.toString().padStart(2, '0');
        countdownElement.html(countdownString);
        
        remainingTime--;
    }, 1000);
});
