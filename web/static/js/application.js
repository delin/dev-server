$(document).ready(function() {
  //~ var is_create = [];

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

  setInterval(function()
  {
    var jqxhr = $.getJSON('/ajax/nodes_stat.json',
      function(data) {
        i = 0;
        for (node in data)
        {
          $("#node"+i+"_stat-load_avarage").text(data[node].load_avarage[0] + ", " + data[node].load_avarage[1] + ", " + data[node].load_avarage[2]);
          $("#node"+i+"_stat-date").text(data[node].date);
          $("#node"+i+"_stat-uptime").text(data[node].uptime);
          $("#node"+i+"_stat-services").text(data[node].services);

          red = (Math.round(255 * data[node].cpu_percent / 100)).toString(16);
          green = (Math.round(255 * (100 - data[node].cpu_percent) / 100)).toString(16);
          $("#node"+i+"_stat-cpu_percent").css('background-color', "#" + red + green + "00");

          red = (Math.round(255 * data[node].mem_percent / 100)).toString(16);
          green = (Math.round(255 * (100 - data[node].mem_percent) / 100)).toString(16);
          $("#node"+i+"_stat-mem_percent").css('background-color', "#" + red + green + "00");

          red = (Math.round(255 * data[node].disk_percent / 100)).toString(16);
          green = (Math.round(255 * (100 - data[node].disk_percent) / 100)).toString(16);
          $("#node"+i+"_stat-disk_percent").css('background-color', "#" + red + green + "00");

          $("#node"+i+"_stat-cpu_percent").css('width', data[node].cpu_percent + '%');
          $("#node"+i+"_stat-cpu_percent-label").text(data[node].cpu_percent + '%');
          $("#node"+i+"_stat-mem_usage").text(data[node].mem_usage + "/" + data[node].mem_total + "Mb");
          $("#node"+i+"_stat-mem_percent").css('width', data[node].mem_percent + '%');
          $("#node"+i+"_stat-swap_usage").text(data[node].swap_usage + "/" + data[node].swap_total + "Mb");
          $("#node"+i+"_stat-swap_percent").css('width', data[node].swap_percent + '%');
          $("#node"+i+"_stat-disk_usage").text(data[node].disk_usage + "/" + data[node].disk_total + "Gb");
          $("#node"+i+"_stat-disk_percent").css('width', data[node].disk_percent + '%');
          $("#node"+i+"_stat-procs_total").text(data[node].procs_total);
          i++;
        }
      }
    )
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
