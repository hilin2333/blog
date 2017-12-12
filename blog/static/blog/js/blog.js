$(function (){
    $('a','.toc').on('click',function (e) {
        var idSelector = $(e.target).attr("href");
        window.location.hash =  idSelector;
        $(window).scrollTop($(idSelector).offset().top - 60);
        e.preventDefault();
    });
    var url = window.location.href;
    var index = url .lastIndexOf("\/");
    var id  = url .substring(index + 1, url .length);
    var aHref = $("a\[href='"+ id +"']");
    if(aHref.length > 0){
        aHref.trigger("click");
    }
    // search form
    $('#js-search-btn').on('click', function (e) {
        var $musk = $('#search-musk');
        var $searchForm = $('#search-form');

        if ($musk.length === 0) {
            // Musk does not exist, create it.
            $musk = $('<div></div>')
                .addClass('musk')
                .attr('id', 'search-musk')
                .appendTo($searchForm)
                .click(function () {
                    $searchForm.slideUp();
                    $(this).fadeOut();
                });
        }

        $searchForm.removeClass('hide-on-mobile')
            .hide().slideDown()
            .find('input')
            .focus();
        $musk.fadeIn();

        return false;
    });

    // sidebar
    $('#js-sidebar-btn').on('click', function (e) {
        var $musk = $('#sidebar-musk');
        var $sideBar = $('.toc-sidebar');

        if ($musk.length === 0) {
            // Musk does not exist, create it.
            $musk = $('<div></div>')
                .addClass('musk')
                .attr('id', 'sidebar-musk')
                .css('z-index', 1)
                .appendTo('body')
                .click(function () {
                    $(this).fadeOut(500);
                    $sideBar.animate({'left': '-70%'}, 500);
                });
        }
        $sideBar.animate({'left': 0}, 500);
        $musk.fadeIn(500);
        return false;
    });

    // back top
    var $backTop = $('.back-top');

    if ($backTop.length === 0) {
        // Button back top does not exist, create it.
        $backTop = $('<a href="#" class="back-top"><i class="fa fa-arrow-up" aria-hidden="true"></i></a>')
            .appendTo('body')
            .click(function (e) {
                if ($(window).scrollTop() > 0 && !$('html,body').is(':animated')) {
                    $('html,body').animate({scrollTop: 0}, 500);
                }
                return false
            });
    }

    $(window).on('scroll', function (e) {
        var $pos = $(window).height() / 2;
        if ($(window).scrollTop() > $pos) {
            $backTop.fadeIn();
        } else {
            $backTop.fadeOut();
        }
    });

    // reward
    $('#js-reward').click(function () {
        var $this = $(this);
        $this.next().slideToggle()
    })
    var classes = ["tag-1", "tag-2", "tag-3", "tag-4", "tag-5"];
    $("#tagCloud a").each(function(){
        $(this).addClass(classes[~~(Math.random()*classes.length)]);
    });
    (function () {
    // 更新底栏的位置，当页面内容高度小于窗口高度时，会将底栏浮动定位在窗口底端
    function updateFooterPosition() {
      var pageHeight = document.body.offsetHeight;
      if ($footer.hasClass('fixed-bottom')) {
        pageHeight += $footer.outerHeight();
        if (pageHeight > $(window).height()) {
          $footer.removeClass('fixed-bottom');
        }
      } else {
        if (pageHeight < $(window).height()) {
          $footer.addClass('fixed-bottom');
        }
      }
    }
    var $footer = $('#my_footer');
    $(document).on('ready', updateFooterPosition);
    $(window).on({
      'scroll': updateFooterPosition,
      'resize': updateFooterPosition
    });
    // 每隔一段时间检测页面高度变化，确保底栏能在页面最底端
    setInterval(updateFooterPosition, 500);
  })();
});
 $('[data-menu]').menu();

    var InterValObj; //timer变量，控制时间
    var curCount = 120;//当前剩余秒数

    $('#js-send').on('click', function (event) {
        var $this = $(this);
        var $targetURL = $this.attr('data-target');
        $.post(
            $targetURL,
            {email: $('#id_email').val()},
            function (data) {
                if (data.ok) {
                    $this.attr("disabled", "true");
                    $this.text("重新发送验证码" + "(" + curCount + ")");
                    InterValObj = window.setInterval(SetRemainTime, 1000); //启动计时器，1秒执行一次
                    $('.message')
                        .find('span')
                        .text(data.msg)
                } else {
                    $('.message').find('span').text(data.msg)
                }
            }
        );
        return false;
    });

    //timer处理函数
    function SetRemainTime() {
        if (curCount === 0) {
            window.clearInterval(InterValObj);//停止计时器
            $('#js-send').removeAttr("disabled");//启用按钮
            $('#js-send').text("重新发送验证码");
        }
        else {
            curCount--;
            $('#js-send').text("重新发送验证码" + "(" + curCount + ")");
        }
    }

    $('#js-submit').on('click', function (event) {
        var $this = $(this);
        var $form = $('.email-binding-form');
        var $targetURL = $form.attr('action');
        console.log($targetURL);

        $.post(
            $targetURL,
            {
                email: $('#id_email').val(),
                verification_code: $('#id_verification_code').val()
            },
            function (data) {
                if (data.ok) {
                    location.reload();
                } else {
                    $('.message')
                        .find('span')
                        .text(data.msg)
                }
            }
        );
        return false;
    });
    var $editor = $('#id_comment');
    if($editor.length > 0){
        $(function () {
            $editor.markdown({
                language: 'zh',
                imgurl: "/api/upload/",
		hiddenButtons:['cmdEmoji']
            }).attr("placeholder","提出你的见解...");
            $editor.on("drop", function (e) {
                e.preventDefault();
                e.stopPropagation();

                var fileList = e.originalEvent.dataTransfer.files;
                if (fileList.length == 0) {
                    return;
                }
                if (fileList[0].type.indexOf('text') != -1) {
                    if (fileList[0].size > 1024 * 100) {
                        alert("文本文件不能超过100k");
                        return;
                    }
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        var contents = e.target.result;
                        var old_content = $editor.val();
                        $editor.val(old_content + contents);
                        var b = jQuery.Event('keyup', {
                            which: 39
                        });
                        $editor.trigger(b);
                    }
                    reader.readAsText(fileList[0]);
                    return;
                }

                if (fileList[0].type.indexOf('image') === -1) {
                    alert("无法上传非图片");
                    return;
                }

                var reader = new FileReader();
                reader.onload = function (e) {
                    $loader.show();
                }
                reader.readAsDataURL(fileList[0]);

                var xhr = new XMLHttpRequest();
                xhr.open("post", "/api/upload", true);
                xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
                xhr.upload.addEventListener("progress",
                    function (e) {
                        if (e.lengthComputable) {
                            var loaded = Math.ceil((e.loaded / e.total) * 100);
                        }
                    },
                    false);

                xhr.addEventListener("load",
                    function (e) {
                        $loader.hide();

                        var i = $.parseJSON(e.target.response);
                        var val = $editor.val();
                        val += '![输入图片说明](' + i.files[0].url + ' "在这里输入图片标题")';
                        $editor.val(val);
                        var b = jQuery.Event('keyup', {
                            which: 39
                        });
                        $editor.trigger(b);
                    },
                    false);

                xhr.setRequestHeader("Cache-Control", "no-cache");
                xhr.setRequestHeader('X-CSRFToken', $('meta[name="csrf-token"]').attr('content'));
                xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

                var fd = new FormData();
                fd.append('files', fileList[0]);
                xhr.send(fd);
            });
        })
    }
