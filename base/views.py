from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Note

@login_required
def homePage(request):
  user = request.user
  users = User.objects.all()
  notes = Note.objects.filter(Q(receiver=user) | Q(sender=user))

  # Group messages by contact
  notesByContact = {}
  for note in notes:
    contact = note.sender
    if note.sender == user:
      contact = note.receiver

    if contact in notesByContact:
      notesByContact[contact].append(note)
    else:
      notesByContact[contact] = [note]

  content ={'users': users, 'notesByContact' : notesByContact}
  return render(request, 'pages/index.html', content)


def addNote(request):
  sender = User.objects.get(username = request.user)
  receiver = User.objects.get(username=request.GET.get('to'))
  content = request.GET.get('content')

  #note = Note.objects.create(sender=sender, receiver=receiver, content=content)

  import sqlite3
  from django.utils.timezone import now
  try:
    connection = sqlite3.connect('db.sqlite3')
    dateString = f"{now().date()} {now().time()}"
    query = f"INSERT INTO base_note(sender_id, receiver_id, created_at, readByReceiver, content) VALUES ({sender.id}, {receiver.id}, '{dateString}', 0, '{content}')"
    print(query)
    crsr = connection.cursor()
    crsr.executescript(query)
    connection.commit()
  except sqlite3.Error as error:
    print("Database error", error)

  return redirect('/')

@login_required
def deleteNote(request):
  note_id = request.GET.get('id')
  Note.objects.filter(id=note_id).delete()
  return redirect('/')

# @login_required
# def deleteNote(request):
#   user = User.objects.get(username = request.user)
#   note_id = request.GET.get('id')
#   notes = Note.objects.filter(id=note_id)
#   if len(notes) == 0:
#     return redirect('/')
#   note = notes[0]
#   if note.receiver == user:
#     note.delete()
#   return redirect('/')

def registerUser(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('/')
    else:
      return redirect('register')

  form = UserCreationForm()
  contex = {'form' : form}
  return render(request, 'registration/register.html', contex)