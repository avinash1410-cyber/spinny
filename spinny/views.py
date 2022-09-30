from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(('GET','POST'))
def Home(request):
    dictionary={
	"path('/')--->Documentaion                                                                                    ",
        "path('app/my/'),--->Will Show all My Boxes                                                                     ",
        "path('app/login/'),--->For Login                                                                               ", 
        "path('app/logout/'),---->For Logout                                                                            ",
        "path('app/update/'),--->if user is a staff can update boxes                                                    ",
        "path('app/delete/'),---->if user is a creator of box can delte boxes                                           ",
        "path('app/boxAction/'),-->Will Show All boxes if user is staff also show Creator and last update           IF REQUEST IS GET",
        "path('app/boxAction/'),-->Add boxes if user is staff also show Creator and last update                     IF REQUEST IS POST",
        "path('app/filter/'),----->Can Apply filter over boxes dimension                                                ",
        "path('app/my_filter/'),--->Will Show my boxes by filtering by Dimesnion                                        ",
    }
    return Response(dictionary)