from rest_framework import serializers
from blogs.models import Blog, SubBlog
from users.api.serializers import AccountSerializer


class BlogSerializer(serializers.ModelSerializer):


    class Meta:
        model = Blog
        fields = '__all__'


class LikeBlogSerializer(serializers.Serializer):
    blog_id   = serializers.IntegerField()
    like_value  = serializers.IntegerField()


    def validate_like_value(self, like_value):
        if like_value > 0:
            return 1
        else:
            return -1

    
    def validate_blog_id(self, blog_id):
        if Blog.objects.filter(id=blog_id):
            return blog_id
        raise serializers.ValidationError("Blog not found.")


    def validate(self, data):
        user = self.context.get('user')
        blog = Blog.objects.get(id=data['blog_id'])
        if data['like_value'] == 1:
            if user.username in blog.users_who_liked.split('/'):
                raise serializers.ValidationError("You cant like a blog more then once.")
        elif data['like_value'] == -1:
            if not user.username in blog.users_who_liked.split('/'):
                raise serializers.ValidationError("You cant unlike a blog without liking it first.")
        return data


    def update(self, instance, validated_data):
        blog = Blog.objects.get(id=validated_data['blog_id'])
        if validated_data['like_value'] > 0:
            blog.like(instance)
        else:
            blog.dislike(instance)
        return instance


class DeleteSubblogSerializer(serializers.Serializer):
    subblog_title = serializers.CharField(max_length=30)
    parent_blog_id = serializers.IntegerField()


    def validate(self, data):
        if not Blog.objects.get(id=data['parent_blog_id']):
            raise serializers.ValidationError("Couldnt find the blog you provided")
        if not Blog.objects.get(id=data['parent_blog_id']).author == self.context.get('user'):
            raise serializers.ValidationError("You are not the owner of this blog")
        blog = Blog.objects.get(id=data['parent_blog_id'])
        if not SubBlog.objects.filter(parent_blog=blog, title=data['subblog_title']):
            raise serializers.ValidationError(f"You have no subblog named {data['subblog_title']}")
        return data


    def update(self, instance, validated_data):
        blog = Blog.objects.get(id=validated_data['parent_blog_id'])
        subblog = SubBlog.objects.get(title=validated_data['subblog_title'], parent_blog=blog)
        subblog.delete()
        return subblog