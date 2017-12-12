from django.forms import Textarea


class BootstrapMarkdownTextarea(Textarea):
    class Media:
        css = {
            'all': (
                    'https://cdn.bootcss.com/semantic-ui/2.2.13/components/icon.css',
                    'https://cdn.bootcss.com/bootstrap/3.3.6/css/bootstrap.min.css',
                    'blog/markdown/gitee.editor.css',
                    'blog/markdown/gitee.comment.css',
                )
        }
        js = (
            'blog/markdown/gitee.editor.js',
            'blog/markdown/gitee.markdown-zh.js',
        )
