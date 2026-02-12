from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import UserProfile, Ticket, Film
from .serializers import TicketSerializer, UserSerializer

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        
        # 1. Create or Get User
        user, _ = UserProfile.objects.get_or_create(
            mobile_number=data['contact'],
            defaults={
                'name': data['name'],
                'branch': data['branch'],
                'year': data['year']
            }
        )
        
        # 2. Get or Create Film
        film, _ = Film.objects.get_or_create(
            slug=data['film_slug'],
            defaults={
                'title': data['film_title'],
                'date': data['date'],
                'time': data['time'],
                'venue': data['venue']
            }
        )

        # 3. Prevent Duplicate Booking
        if Ticket.objects.filter(user=user, film=film).exists():
             return Response({"message": "Already registered!"}, status=400)

        # 4. Create Ticket (QR generates automatically)
        ticket = Ticket.objects.create(user=user, film=film)
        
        return Response({
            "message": "Success",
            "ticket_id": ticket.id,
            "qr_code": ticket.qr_code.url
        })

class AdminScanView(APIView):
    def post(self, request):
        ticket_id = request.data.get('ticket_id')
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            if ticket.is_checked_in:
                return Response({"status": "error", "message": "ALREADY USED!"})
            
            ticket.is_checked_in = True
            ticket.save()
            return Response({"status": "success", "message": f"Welcome {ticket.user.name}!"})
        except:
            return Response({"status": "error", "message": "Invalid Ticket"})
            
class AdminListView(generics.ListAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = Ticket.objects.all().order_by('-created_at')
        
        # Filter by Film Slug
        film_slug = self.request.query_params.get('film')
        if film_slug:
            queryset = queryset.filter(film__slug=film_slug)
            
        # Filter by Status
        status_param = self.request.query_params.get('status')
        if status_param == 'checked_in':
            queryset = queryset.filter(is_checked_in=True)
        elif status_param == 'pending':
            queryset = queryset.filter(is_checked_in=False)
            
        return queryset

class HealthCheckView(APIView):
    """
    Simple endpoint to keep the server alive.
    """
    def get(self, request):
        return Response({"status": "alive", "message": "Server is running"})

class MyTicketsView(generics.ListAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        mobile = self.request.query_params.get('mobile')
        if not mobile:
            return Ticket.objects.none()
        return Ticket.objects.filter(user__mobile_number=mobile).order_by('-created_at')