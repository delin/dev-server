$(document).ready(function() {
  $('#modal-web_off').modal({
    keyboard: false,
    show: false
  });

  setInterval(function()
  {
    var jqxhr = $.getJSON('/ajax/sys_stat.json',
      function(data) {
        $('#modal-web_off').modal('hide');

        $("#sys_stat-load_avarage").text(data.sys_stats.load_avarage[0] + ", " + data.sys_stats.load_avarage[1] + ", " + data.sys_stats.load_avarage[2]);
        $("#sys_stat-date").text(data.sys_stats.date);
        $("#sys_stat-uptime").text(data.sys_stats.uptime);

        red = (Math.round(255 * data.sys_stats.cpu_percent / 100)).toString(16);
        green = (Math.round(255 * (100 - data.sys_stats.cpu_percent) / 100)).toString(16);
        $("#sys_stat-cpu_percent").css('background-color', "#" + red + green + "00");

        red = (Math.round(255 * data.sys_stats.mem_percent / 100)).toString(16);
        green = (Math.round(255 * (100 - data.sys_stats.mem_percent) / 100)).toString(16);
        $("#sys_stat-mem_percent").css('background-color', "#" + red + green + "00");

        red = (Math.round(255 * data.sys_stats.disk_percent / 100)).toString(16);
        green = (Math.round(255 * (100 - data.sys_stats.disk_percent) / 100)).toString(16);
        $("#sys_stat-disk_percent").css('background-color', "#" + red + green + "00");

        $("#sys_stat-cpu_percent").css('width', data.sys_stats.cpu_percent + '%');
        $("#sys_stat-cpu_percent-label").text(data.sys_stats.cpu_percent + '%');
        $("#sys_stat-mem_usage").text(data.sys_stats.mem_usage + "/" + data.sys_stats.mem_total + "Mb");
        $("#sys_stat-mem_percent").css('width', data.sys_stats.mem_percent + '%');
        $("#sys_stat-swap_usage").text(data.sys_stats.swap_usage + "/" + data.sys_stats.swap_total + "Mb");
        $("#sys_stat-swap_percent").css('width', data.sys_stats.swap_percent + '%');
        $("#sys_stat-disk_usage").text(data.sys_stats.disk_usage + "/" + data.sys_stats.disk_total + "Gb");
        $("#sys_stat-disk_percent").css('width', data.sys_stats.disk_percent + '%');
        $("#sys_stat-procs_total").text(data.sys_stats.procs_total);
      })
    .error(function() {
      $('#modal-web_off').modal('show');
    })
  }, 2000);
});

//~ // button state demo
//~ $('#fat-btn-srv1-stop')
  //~ .click(function () {
    //~ var btn = $(this)
    //~ btn.find('span').text('Stopping…')
    //~ btn.addClass('disabled');
    //~ setTimeout(function () {
      //~ btn.find('span').text('Stop')
      //~ btn.removeClass('disabled');
    //~ }, 3000)
  //~ })
//~
//~ $('#fat-btn-srv1-restart')
  //~ .click(function () {
    //~ var btn = $(this)
    //~ btn.find('span').text('Restarting…')
    //~ btn.addClass('disabled');
    //~ setTimeout(function () {
      //~ btn.find('span').text('Restart')
      //~ btn.removeClass('disabled');
    //~ }, 3000)
  //~ })
