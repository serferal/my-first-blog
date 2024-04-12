from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'imagen']

    def save(self, commit=True):
        post = super().save(commit=False)
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            post.imagen_data = imagen.file.read()  # Convertir la imagen a bytes y almacenarla en el campo imagen_data
        if commit:
            post.save()
        return post
