#include <iostream>
#include <math.h>
#include <stdlib.h>


using namespace std;
typedef struct poin{
       int x;
       int y;
       }point;
typedef struct distanc{
       point l;
       point r;
       double dis;
       }distan;
double ftd(point a,point b)
{
       double c=(a.x-b.x)*(a.x-b.x)+(a.y-b.y)*(a.y-b.y);
       return  sqrt(c);
}
int compare(const void *elem1,const void *elem2)
{
	struct poin *c=(poin *)elem1;
	struct poin *d=(poin *)elem2;
	if(c->x != d->x) return c->x-d->x;
   	else return d->y - c->y;

}
distan findmin(point innerp[],int num)
{
         if(num==3)
         {
                   double dis1=ftd(innerp[0],innerp[1]);
                   double dis2=ftd(innerp[1],innerp[2]);
                   distan thisis;
                   if(dis1<=dis2)
                   {
                                 thisis.l=innerp[0];
                                 thisis.r=innerp[1];
                                 thisis.dis=dis1;
                   }
                   else
                   {
                                 thisis.l=innerp[1];
                                 thisis.r=innerp[2];
                                 thisis.dis=dis2;
                                 
                   }
                  // cout<<thisis.dis<<" ";
				   return thisis;
         }
         if(num==2)
         {
                   distan thisis;
                   thisis.l=innerp[0];
                   thisis.r=innerp[1];
                   thisis.dis=ftd(innerp[0],innerp[1]);
                   //cout<<thisis.dis<<" ";
				   return thisis;
         }
         else
         {
              int num1=num/2;
              int num2=num-num1;
              point p1[101];
              point p2[101];
              for (int j1=0;j1<num;j1++)
              {
                  if(j1<num1)
                  {
                             p1[j1]=innerp[j1];
                            // cout<<"  "<<p1[j1].x<<" "<<p1[j1].y; 
                  }
                  else
                  {
                             p2[j1-num1]=innerp[j1];
                           // cout<<"  "<<p2[j1-num1].x<<" "<<p2[j1-num1].y;
                  }
              }
                  
              distan thisis1=findmin(p1,num1);
              distan thisis2=findmin(p2,num2);
              distan thisis3;
			  if(thisis1.dis<thisis2.dis)
			  {
					thisis3=thisis1;
			  }
			  else
			  {
					thisis3=thisis2;
			  }
			  //cout<<" "<<p2[0].x<<" "<<p1[num1-1].x<<" ";
              double mid=((p2[0].x+p1[num1-1].x)/2.0);
              //cout<<"mid="<<mid<<" ";
			  point p3[101];
			  point p4[101];
			  int j3=0;
			  int j4=0;
			  for(int j2=0;j2<num;j2++)
			  {
				  if(j2<num1)
				  {
					  if((mid-p1[j2].x)<=thisis3.dis)
						  p3[j3]=p1[j2];
						  j3++;
				  }
				  else
				  {
					  if((p2[j2-num1].x-mid)<=thisis3.dis)
						  p4[j4]=p2[j2-num1];
					      j4++;
				  }
			  }
			  if(j3==0||j4==0)
				  return thisis3;
			  distan thisis4=thisis3;
			  for(int j5=0;j5<j3;j5++)
			  {
				  for(int j6=0;j6<j4;j6++)
					  if(labs(p4[j6].y-p3[j5].y)<=thisis3.dis)
					  {
						  double disdis=ftd(p4[j6],p3[j5]);
						  if(disdis<thisis4.dis)
						  {
							  thisis4.dis=disdis;
							  thisis4.l=p3[j5];
							  thisis4.r=p4[j6];
							 // cout<<" p3[j5].x="<<p3[j5].x;
							 // cout<<" p3[j5].y="<<p3[j5].y;
							 // cout<<" p4[j6].x="<<p4[j6].x;
							 // cout<<" p4[j6].y="<<p4[j6].y;
						  }
					  }
			  }
			  //cout<<thisis4.dis<<" ";
			  return thisis4;
		 }
}
						  
              
              
                   
                   
int main()
{
    int nummber;
    cout<<"请输入点的数目：\n";
    cin>>nummber;
    point p[101];
    cout<<"请输入点的x和y坐标：\n";
    for(int i=0;i<nummber;i++)
    {
            cin>>p[i].x>>p[i].y;
    }
    qsort(p,nummber,sizeof(poin),compare);
/*    for(int i1=0;i1<(nummber-1);i1++)
    {
            for(int i2=0;i2<nummber-i1-1;i2++)
            {
                   if(p[i2].y<p[i2+1].y||(p[i2].y==p[i2+1].y&&p[i2].x>p[i2+1].x))
                   {
                                                                                                         p[nummber]=p[i2];
                                                                                                         p[i2]=p[i2+1];
                                                                                                         p[i2+1]=p[nummber];
                   }
            }
    }*/ 
/*	for(int i3=0;i3<nummber;i3++)
	{
  	cout<<p[i3].x<<" "<<p[i3].y<<endl;
	}*/   
    distan d=findmin(p,nummber);
    //cout<<"\n"<<d.dis;
    cout<<"一个点的坐标是: "<<d.l.x<<" "<<d.l.y<<" ; 另一个点的坐标是: " <<d.r.x<<" "<<d.r.y;
    system("pause");
}
