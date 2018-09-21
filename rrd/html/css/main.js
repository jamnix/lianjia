/*  
 *
 * 网站的JS脚本写在这
 *
 */


/* 调试开关，保证ie不回报错 */
//var DEBUG = true;
var DEBUG = false;

if (! window.console && !DEBUG ) {
    window.console = {
        log:   function() {}, warn:  function() {},
        error: function() {}, fatal: function() {},
        debug: function() {}, dir:   function() {}
    }
}

// 线上
var Server = "http://stat.vip.xunlei.com/stat/display/";
// 调试
// var Server = "http://stat.display.xunlei.com/stat/display/";
var Project = "project=cloud_vod";
//Project = "project=lixian";
var TableData = {
    meta: {},
    data:{},
    column:{}
};

var CurTableName;



function create_req_obj(server, interface, query, callback){
    return {
        url: server + interface + '?' + query,
        dataType: "jsonp",
        jsonp: "jsonp",
        success: callback
    };
}





function build_list(data){
    /* 获取并清空目标节点,然后填充数据 */
    var root = $("#chart_list ul");
    //console.log("root:", root);

    var meta_list = data.meta_list;
    if(meta_list.length == 0)
        return;
    root.empty();

    /* 排序 */
    var a, b, temp;
    for(var i=0; i<meta_list.length; ++i){
        for(var j=i+1; j<meta_list.length; ++j){
            a = meta_list[i];
            b = meta_list[j];
            /* 比较对象内的标签名 */
            if(a[1] > b[1]){
                temp = meta_list[i];
                meta_list[i] = meta_list[j];
                meta_list[j] = temp;
            }
        }
    }


    var add_element, element;
    for(var i=0; i<meta_list.length; ++i){

        var table_name = meta_list[i][0];   /* 表名 */
        var text_name = meta_list[i][1];   /* 标签名 */
        var detail_name = meta_list[i][2];   /* 说明 */

        var name = meta_list[i][1];   /* 标签名 */
        //console.log("name:", name);
        /* 根据数据标识 '>' 来创建分别创建列表 */
        var index = name.indexOf('>');
        //console.log("index:", index);


        /* 只有一级菜单的情况 */
        if(index == -1){
            add_element = $("<li><a></a></li>")
            element = add_element.find("a");

            element.text(decode(text_name));
            element.attr("href", "javascript:;");
            element.attr("title", detail_name);
            element.attr("table_name", table_name);

            root.append(add_element);
        }
        else{
            var parent_name, childname;

            parent_name = name.substring(0,index);
            childname = name.substring(index+1);
            //console.log("parent_name:", parent_name);
            //console.log("childname:", childname);

            /* 判断父级目录是否存在 */
            var query = 'li[folder_name=' + parent_name + ']';
            var ret = root.children(query);
            /* 没有父目录则创建 */
            if(ret.length == 0){
                add_element = $("<li>" + parent_name +"</li>");
                add_element.attr("folder_name", parent_name);

                element = $("<ul><li><a></a></li></ul>");
                var ele = element.find("a");
                ele.text(decode(childname));
                ele.attr("href", "javascript:;");
                ele.attr("title", detail_name);
                ele.attr("table_name", table_name);

                add_element.append(element);
                root.append(add_element);
            }
            else{
                add_element = $("<li><a></a></li>");
                element = add_element.find("a");
                element.text(decode(childname));
                element.attr("href", "javascript:;");
                element.attr("title", detail_name);
                element.attr("table_name", table_name);

                ret.children('ul').append(add_element);
            }


        }

    }


}
function decode(str){
    try{
        return decodeURIComponent(str);
    }catch(e){
        try{
            return decodeURI(str);
        }catch(e){
            return str;
        }       
    }

}


function get_list(){

    var list_back = function(data){
        console.log("data:", data);

        if(data.resp.ret != 0)
            return;

        build_list(data.resp);

        /* 这里自动触发第一个 */
        $('#chart_list ul li a').eq(0).click();


    }

    var obj = create_req_obj(Server, "list", Project, list_back);
    $.ajax(obj);

}



function quick_query(){
    var now, past, start, end;

    now = new Date();
    start = end = now.getTime();

    var day_ms = 24*3600*1000;

    var select = $(this).attr("recent");
    //console.log("select:", select);
    switch(select){
        case 'week':
            start = end - 7 * day_ms;
            break;
        case 'hmonth':
            start = end - 15 * day_ms;
            break;
        case 'hhyear':
            start = end - 92 * day_ms;
            break;
        case 'hyear':
            start = end - 183 * day_ms;
            break;
    }

    past = new Date(start);


    var start_yy, start_mm, start_dd;
    var end_yy, end_mm, end_dd;
    var start_date, end_date, query_date;

    start_yy = past.getFullYear();
    start_mm = past.getMonth() + 1;
    if(start_mm < 10)
        start_mm = '0' + start_mm;
    start_dd = past.getDate();
    if(start_dd < 10)
        start_dd = '0' + start_dd;

    end_yy = now.getFullYear();
    end_mm = now.getMonth() + 1;
    if(end_mm < 10)
        end_mm = '0' + end_mm;
    end_dd = now.getDate();
    if(end_dd < 10)
        end_dd = '0' + end_dd;

    start_date = start_yy + '-' + start_mm + '-' + start_dd;
    end_date = end_yy + '-' + end_mm + '-' + end_dd;

    query_date = start_date + '_' + end_date;
    //console.log("query_date:", query_date);

    get_table(CurTableName, query_date);

}





function build_list_event(){
    $('#chart_list ul li a').live('click', function() {
        /* 取消上次选中样式，挂接选中项样式 */
        $('#chart_list ul li a').each(function(){
            $(this).removeClass('cur');
        });
        $(this).addClass('cur');

        var table_name = $(this).attr("table_name");
        console.log("table_name:", table_name);
        get_table(table_name);
    });

    /* 挂接确定键事件 */
    $('#enter_btn').live('click', function() {
        get_table(CurTableName);
    });

    /* 挂接快速查询按钮 */
    $('#quick_btn a').live('click', quick_query);

}



function save_meta(){
    $('#chart_list ul li a').live('click', function() {
        var table_name = $(this).attr("table_name");
        console.log("table_name:", table_name);
        get_table(table_name);

    });
}




function order_field(){
    var thead = $("#chart_table thead");

    /* 判断是否有 '>' 确定是否需要分类显示 */
    var mark = false;    /* 标识是否存在 '>' */
    var ret = 0;
    var first_row = thead.children('tr').eq(0);
    var elements = first_row.children('th');
    console.log("first_row:", first_row);
    /* 遍历检测 */
    for(var i=0; i<elements.length; ++i){
        ret = elements.eq(i).text();
        if(ret.indexOf('>') != -1)
            mark = true;
    }
    console.log("mark:", mark);
    if(mark == false)
        return;


    /* 处理名称，建立双行结构,填充第二行或合并行 */
    var second_row = $("<tr></tr>");
    for(var i=0; i<elements.length; ++i){
        elements.eq(i).attr('colspan', 1);  /* 建立colspan，下一个for要用到 */

        var name = elements.eq(i).text();
        var index = name.indexOf('>');
        if(index == -1){
            elements.eq(i).attr('rowspan', 2);
        }
        else{
            var parent_name = name.substring(0,index);
            var childname = name.substring(index+1);

            elements.eq(i).text(parent_name);
            var element = $("<th></th>");
            element.text(childname);

            second_row.append(element);
        }

    }
    thead.append(second_row);


    /* 字段相同，则字段（列） */
    for(var i=0; i<elements.length; ++i){
        var first = elements.eq(i);

        for(var j=i+1; j<elements.length; ++j){
            var second = elements.eq(j);
            if(first.text() == second.text()){
                var colspan = first.attr('colspan');
                colspan = parseInt(colspan);
                colspan += 1;
                first.attr('colspan', colspan);
                second.remove();
            }
        }
    }

}


function highlight_weekend(){
    /* 找到所有日期项 */
    dates = [];
    var tr = $("#chart_table tbody tr");
    tr.each(function(){
        var ele = $(this).find("td:first")[0];
        dates.push(ele);
    });

    //console.log("dates:", dates);
    /* 如果对应的日期项是周末，则挂接样式 */
    for(var i=0; i<dates.length; ++i){
        var item = $(dates[i]);
        var text = item.text();

        /* 用 '-' 符号初步判断是不是日期 */
        if(text.indexOf('-') == -1)
            return;

        var time = new Date(text);
        var today = time.getDay();
        if(today == 0){
            item.addClass('weekend');
            item.attr("title", "星期天");
        }
        if(today == 6){
            item.addClass('weekend');
            item.attr("title", "星期六");
        }

        //console.log("time:", time);



    }

}


function build_table(column){
    /* 获取并清空目标节点,然后填充数据 */
    var root = $("#chart_table");
    var thead = root.find("thead");
    var tbody = root.find("tbody");
    console.log("thead:", thead);

    /* 先隐藏表格，如果有错误，则不显示 */
    root.hide();

    if(column.length == 0)
        return;

    /* 清空并填充字段名 */
    thead.empty();
    var element;
    var item = $("<tr></tr>");
    for(var i=0; i<column.length; ++i){
        var text_name = column[i].name;   /* 标签名 */
        var detail_name = column[i].description;   /* 说明 */

        element = $("<th></th>");
        element.text(decode(text_name));
        element.attr("title", detail_name);

        item.append(element);
    }
    thead.append(item);

    /* 清空并填充数据 */
    tbody.empty();
    /* 先按主键填充行数tr */
    var primary_key = column[0];
    for(var i=0; i<primary_key.data.length; ++i){
        element = $("<tr></tr>");
        tbody.append(element);
    }

    /* 再一列列填充 */
    var col;
    var tr = tbody.children('tr');
    for(var i=0; i<column.length; ++i){
        col = column[i].data;
        for(var j=0; j<col.length; ++j){
            var column_name = column[i].name;   /* 该列的名字*/
            var data = column[i].data[j];
            // 对百分比的数据加加百分号
            if(column_name.indexOf("%") != -1)
                data = data.toFixed(2) + "%";
            element = $("<td></td>");
            element.text(data);

            tr.eq(j).append(element);
        }
    }

    order_field();
    highlight_weekend();

    root.show();
}





function build_chart(column){
    //console.log("head_data:", head_data);

    /* 获取主键的列，现在默认为第一列 */
    var primary_key = column[0];
    /* 复制对象 */
    var categories = [];
    $.extend(categories, primary_key.data);
    categories = categories.reverse();

    //console.log("categories:", categories);
    //console.log("primary_key:", primary_key.data);


    var series = [];
    for(var i=1; i<column.length; ++i){
        var obj = {};
        obj.name = column[i].name;
        obj.data = [];
        // 只显示前面十条曲线
        if(i > 10)
            obj.visible = false;

        for(var j=0; j<column[i].data.length; ++j){
            obj.data.unshift(parseFloat(column[i].data[j]));
        }

        series.push(obj);
    }

    //console.log("series:", series);

    var text_name;
    text_name = column.table_name;   /* 标签名 */

    /* 设置x轴的距离 */
    var xIntervalNum = 5;    /* x轴的坐标点数量 */
    var xInterval = 1;
    if(categories.length > xIntervalNum)
        xInterval = Math.round(categories.length / xIntervalNum);

    var chart = new Highcharts.Chart({
        chart: {
            renderTo: 'chart_canvas',
            type: 'line'
        },
        title: {
            text: text_name,
            x: -20 //center
        },
        xAxis: {
            tickInterval: xInterval,
            labels: {
                rotation: 3,
                align: 'left',
                style: {
                    font: 'normal 11px Arial, sans-serif"'
                }
            },
            categories: categories
        },

        tooltip: {
            style: {
                fontWeight: 'bold'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -10,
            y: 100
        },
        series: series
    });


    // 一键取消查看全部字段或者一键查看全部字段
    var seriesChooseBtn = $("#seriesChooseBtn");
    seriesChooseBtn.attr("chartShow", "true").text('隐藏全部字段');
    seriesChooseBtn.unbind("click").click(function() {
        var btn = $(this);
        var series = chart.series;
        // console.log("series:", chart.series);

        // 调用Highcharts的series里面元素的hide和show方法控制显示
        if (btn.attr("chartShow") == "false") {
            $.each(series, function(){ this.show(); });
            btn.attr("chartShow", "true");
            btn.text('隐藏全部字段');
        } else {
            $.each(series, function(){ this.hide(); });
            btn.attr("chartShow", "false");
            btn.text('显示全部字段');
        }
    });

}


function get_date_range(){
    var root, start_date, end_date;

    root = $("#chart_date");
    start_date = root.find("#from").val();
    end_date = root.find("#to").val();

    start_date = $.trim(start_date);
    end_date = $.trim(end_date);

    if(start_date == '' || end_date == '')
        return null;

    return start_date + '_' + end_date;
}



function column_data(table_data){
    var meta, data, col_data;

    meta = table_data.meta;
    data = table_data.data;

    col_data = [];    /* 每一列为其中一项 */

    console.log("1.mata:", meta);
    console.log("2.data:", data);

    /* 从meta[0]中获取表信息 */
    col_data.table_name = meta[0][1];
    col_data.table_description = [0][2];

    /* 先遍历meta表建立各个字段 */
    /* 根据协议，第一个字段从1开始 */
    for (var i=1; i < meta.length; i++){
        var obj = {
            field: meta[i][0],
            name: meta[i][1],
            description: meta[i][2],
            data: []
        };
        col_data.push(obj);
    }

    /* 再向各个字段填充数据 */
    for (var i=0; i < data.length; i++){
        var row = data[i];
        /* 填充一行 */
        for(var j=0; j < col_data.length; j++){
            /* 在这里处理比例数据（带符号'%'的乘100） */
            var content = row[j];
            if(col_data[j].name.indexOf('%') != -1){
                content = 100 * content;
                content = content.toFixed(2);
                content = parseFloat(content);
            }
            col_data[j].data.push(content);
        }
    }

    console.log("col_data:", col_data);
    return col_data;
}




function get_table(item, query_date){

    var data_back = function(data){
        console.log("data:", data);

        if(data.resp.ret != 0)
            return;

        TableData.data = data.resp.data_list;

        /* 将数据转换成一列一列的 */
        var column = column_data(TableData);
        TableData.column = column;

        build_table(column);
        /* 输出图表 */
        build_chart(column);


    }

    var meta_back = function(data){
        console.log("mata:", data);

        if(data.resp.ret != 0)
            return;

        TableData.meta = data.resp.field_list;


        var date_range = get_date_range();
        //console.log("date_range1:", date_range);
        if(query_date != undefined)
            date_range = query_date;
        //console.log("date_range2:", date_range);
        if(!date_range)
            date_range = '';
        else
            date_range = "&dt=" + date_range;
        var query = Project + "&item="+ item + date_range;
        /* 再去获取data */
        var obj = create_req_obj(Server, "data", query, data_back);
        $.ajax(obj);

    }

    /* 将当前请求的item存入变量 */
    CurTableName = item;

    /* 获取meta成功后，再去获取data */
    var obj = create_req_obj(Server, "meta", Project + "&item="+item, meta_back);
    $.ajax(obj);

}



function getQueryStringArgs(){
    //get query string without the initial ?
    var qs = (location.search.length > 0 ? location.search.substring(1) : "");

    //object to hold data
    var args = {};

    //get individual items
    var items = qs.split("&");
    var item = null,
        name = null,
        value = null;

    //assign each item onto the args object
    for (var i=0; i < items.length; i++){
        item = items[i].split("=");
        name = decodeURIComponent(item[0]);
        value = decodeURIComponent(item[1]);
        args[name] = value;
    }

    return args;
}


function get_project(){
    var query = getQueryStringArgs();

    var project = "project=cloud_vod";

    if(query.project){
        project = "project=" + query.project;
    }
    else
        project = "project=cloud_vod";

    //console.log("query:", query);
    //console.log("project:", project);
    Project = project;
}



$(document).ready(function() {
    get_project();
    get_list();
    build_list_event();


    var dates = $( "#from, #to" ).datepicker({
        defaultDate: "+0w",
        changeMonth: true,
        numberOfMonths: 2,
        showButtonPanel: true,
        onSelect: function( selectedDate ) {
            var option = this.id == "from" ? "minDate" : "maxDate",
                instance = $( this ).data( "datepicker" ),
                date = $.datepicker.parseDate(
                    instance.settings.dateFormat ||
                        $.datepicker._defaults.dateFormat,
                    selectedDate, instance.settings );
            dates.not( this ).datepicker( "option", option, date );
        }
    });
    $( "#from, #to" ).datepicker( "option", "dateFormat", "yy-mm-dd" );

});





