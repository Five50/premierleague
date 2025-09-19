class TranslatableContent:
    """Mixin to provide translatable content fields."""

    def get_translated_field(self, field_name, language=None):
        """Get field value in specified language or fallback to default."""
        from django.utils.translation import get_language

        if language is None:
            language = get_language()

        # Try to get field in requested language
        translated_field = f"{field_name}_{language}"
        if hasattr(self, translated_field):
            value = getattr(self, translated_field)
            if value:
                return value

        # Fallback to Swedish (default)
        swedish_field = f"{field_name}_sv"
        if hasattr(self, swedish_field):
            value = getattr(self, swedish_field)
            if value:
                return value

        # Fallback to base field without language suffix
        if hasattr(self, field_name):
            return getattr(self, field_name)

        return ""
