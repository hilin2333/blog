----

## 在本地运行项目

1. 克隆项目到本地

   打开命令行，进入到保存项目的文件夹，输入如下命令：

   ```
   git clone https://github.com/zmrenwu/django-zmrenwu-blog.git
   ```

2. 创建并激活虚拟环境

   在命令行进入到保存虚拟环境的文件夹，输入如下命令创建并激活虚拟环境：

   ```
   virtualenv blogproject_env

   # windows
   blogproject_env\Scripts\activate

   # linux
   source blogproject_env/bin/activate
   ```

3. 安装项目依赖

   如果使用了虚拟环境，确保激活并进入了虚拟环境，在命令行进入项目所在的 django-zmrenwu-blog 文件夹，运行如下命令：

   ```
   pip install -r requirements/local.txt
   ```

4. 迁移数据库

   在blog中没有migrations文件夹说明未激活modal,有就跳过这一步,激活：
    ```
   python manage.py makemigrations blog users comments notify --settings=blogproject.settings.local
   ```
   在上一步所在的位置运行如下命令迁移数据库：

   ```
   python manage.py migrate --settings=blogproject.settings.local
   ```

5. 创建后台管理员账户

   在上一步所在的位置运行如下命令创建后台管理员账户

   ```
   python manage.py createsuperuser --settings=blogproject.settings.local
   ```

6. 运行开发服务器

   在上一步所在的位置运行如下命令开启开发服务器：

   ```
   python manage.py runserver --settings=blogproject.settings.local
   ```

   在浏览器输入：127.0.0.1:8000

7. 进入后台发布文章

   在浏览器输入：127.0.0.1:8000/admin

   使用第 5 步创建的后台管理员账户登录