class ResponseSerializerMixin:
    response_serializer_class = None

    def get_response_serializer_class(self):
        return self.response_serializer_class

    def get_serializer_context(self):
        return super().get_serializer_context()

    def get_response_serializer(self, *args, **kwargs):
        serializer_class = self.get_response_serializer_class()
        kwargs['context'] = self.get_serializer_context()

        return serializer_class(*args, **kwargs)
