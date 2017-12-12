# -*- coding: utf-8 -*-
from django.forms import Textarea
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
EDITORMD_REDNDER = '''
<style>
.md-grid{
display:grid!important
}
a.deletelink{
    height:auto!important
}
</style>
<script>
    var $editor = $('textarea[name="%s"]');
    if($editor.length > 0){
        $(function () {
            $editor.markdown({
                language: 'zh',
                imgurl: "/api/upload/",
		hiddenButtons:['cmdEmoji'],
                onShow:function(){
                    $('.md-editor').addClass('md-grid');
                },
                onFullscreen:function(){
                    $('.md-editor').removeClass('md-grid');
                    $('a.exit-fullscreen').on('click',function(){
                        $('.md-editor').addClass('md-grid');
                    });
                }
            });
            $editor.css('height','500px'); 
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
                xhr.open("post", "/upload", true);
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
                xhr.setRequestHeader('X-CSRFToken', $('meta[name="csrf-token"]').attr('content')||$('input[name="csrfmiddlewaretoken"]').val());
                xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

                var fd = new FormData();
                fd.append('files', fileList[0]);
                xhr.send(fd);
            });
        })
    }
    </script>
'''

class BodyMdTextarea(Textarea):
    def __init__(self, areaName="", attrs=None):
        super(BodyMdTextarea, self).__init__(attrs)

    class Media:
        css = {
            'all': (
                'https://cdn.staticfile.org/font-awesome/4.3.0/css/font-awesome.css?v=4.3.0',
                'https://cdn.bootcss.com/semantic-ui/2.2.13/components/icon.css',
                'https://cdn.bootcss.com/bootstrap/3.3.6/css/bootstrap.min.css',
                'blog/markdown/gitee.editor.css',
                'blog/markdown/gitee.comment.css',
            )
        }
        js = (
            'https://cdn.staticfile.org/jquery/2.1.4/jquery.min.js',
            'blog/markdown/gitee.editor.js',
            'blog/markdown/gitee.markdown-zh.js',
        )
    def render(self, name, value, attrs=None):
        '''
        关键方法
        :param name:
        :param value:
        :param attrs:
        :return:
        '''
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<textarea{}>\r\n{}</textarea>', flatatt(final_attrs),force_text(value))]
        current_editormd_render = EDITORMD_REDNDER % name
        output.append(current_editormd_render)
        return mark_safe('\n'.join(output))

