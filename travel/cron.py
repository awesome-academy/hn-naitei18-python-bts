from .models import Tour, Booking, Review, Comment
from django.db.models import Count, Sum
import datetime
from django.core.mail import send_mail
import environ
from django.template.loader import render_to_string
env = environ.Env()
environ.Env.read_env()



def sendStatisticEmail():
    today = datetime.date.today()
    prevMonth = today -  datetime.timedelta(days=1)
    prevMonthBooking = Booking.objects.filter(create_date__month = prevMonth.month, create_date__year= prevMonth.year)
    totalBooking =  prevMonthBooking.count()
    totalReview = Review.objects.filter(create_date__month = prevMonth.month, create_date__year= prevMonth.year).count() 
    totalComment = Comment.objects.filter(create_date__month = prevMonth.month, create_date__year= prevMonth.year).count() 
    bestTour = prevMonthBooking.values('tour').annotate(total=Count('id')).order_by('-total')[0]
    tourTitle = Tour.objects.get(id=bestTour['tour']).title
    income = prevMonthBooking.aggregate(Sum('price'))
    income = str(income['price__sum'])
    createDate = today.strftime('%Y-%m-%d')

    context = {
        'totalBooking' : totalBooking,
        'totalReview' : totalReview,
        'totalComment' : totalComment,
        'tourTitle' : tourTitle,
        'income' : income,
        'createDate' : createDate
    }

    html_message = render_to_string("email/statistic.html", context = context)
    message = "Bao cao thang {}".format(today.month)
    send_mail(
        subject='Statistic email',
        message = message,
        html_message= html_message,
        from_email=env('EMAIL_HOST_USER'),
        recipient_list=[env('EMAIL_ADMIN'), ],
    )


