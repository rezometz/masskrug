
$(document).ready(function() {
  $('#calendar').fullCalendar({
    header: {
      left: 'prev,next today',
      center: 'title',
      right: 'month,agendaWeek,agendaDay'
    },
    events: function(start, end, callback) {
      var slugs = $("input[type='checkbox']:checked").toArray();
      var slugs_pk = [];
      for(var i in slugs) {
        slugs_pk.push(slugs[i].value);
      }



      if(typeof calendar_source != 'undefined') {
        url = calendar_source.url;
      }

      $.ajax({   
        url: url,
        data: {  
          pks:   slugs_pk.join(','),
          start: start.getTime(),
          end: end.getTime(),
          csrfmiddlewaretoken: csrf_token,
        },
        method: 'POST',
        success: function(events) {
          callback(events);
        },
      });
    },

  });
  $("input[type='checkbox']").change(function() {
    $('#calendar').fullCalendar('refetchEvents');
  });

});
