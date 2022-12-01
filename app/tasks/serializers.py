from core import models
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


class TagSerializer(ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class TaskSerializer(ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = models.Task
        fields = ['id', 'name', 'remaining_time', 'tags']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, task):
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = models.Tag.objects.get_or_create(
                user=auth_user,
                **tag
            )
            task.tags.add(tag_obj)

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        task = models.Task.objects.create(**validated_data)
        self._get_or_create_tags(tags, task)
        return task

    def update(self, instance, validated_data):
        tags = validated_data.pop['tags', []]
        task = models.Task.objects.create(**validated_data)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, task)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class TaskDetailSerializer(TaskSerializer):
    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['description']
