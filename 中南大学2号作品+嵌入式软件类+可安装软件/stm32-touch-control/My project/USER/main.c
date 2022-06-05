#include "sys.h"
#include "delay.h"
#include "usart.h"
#include "led.h"
#include "key.h"
#include "lcd.h"
#include "timer.h"
#include "string.h"
#include "sdram.h"
#include "touch.h"				
#include "malloc.h"
#include "w25qxx.h"
#include "ff.h"
#include "exfuns.h"
#include "string.h"
#include "sdio_sdcard.h"
#include "fontupd.h"
#include "text.h"
#include "piclib.h"		
#include "math.h"
#include "wm8978.h"	 
#include "audioplay.h"
#include "exti.h"



/************************************************
 ALIENTEK ������STM32F429������ʵ��43
 ͼƬ��ʾʵ��-HAL�⺯����
 ����֧�֣�www.openedv.com
 �Ա����̣�http://eboard.taobao.com  
 ��ע΢�Ź���ƽ̨΢�źţ�"����ԭ��"����ѻ�ȡSTM32���ϡ�
 ������������ӿƼ����޹�˾  
 ���ߣ�����ԭ�� @ALIENTEK
************************************************/

//�õ�path·����,Ŀ���ļ����ܸ���
//path:·��		    
//����ֵ:����Ч�ļ���
void Curtain_Init(){
	LED0=1;
	Show_Str(155,470,240,24,"����״̬���ر�",24,0); 	
	Show_Str(155,495,240,24,"���״̬���ر�",24,0);
	Show_Str(155,520,240,24,"ú����ȫ����ȫ",24,0); 
	Show_Str(155,545,240,24,"�Ŵ�״̬���ر�",24,0);
	Show_Str(155,570,240,24,"���״̬�����",24,0); 		
}
u16 pic_get_tnum(u8 *path)
{	  
	u8 res;
	u16 rval=0;
 	DIR tdir;	 		//��ʱĿ¼
	FILINFO *tfileinfo;	//��ʱ�ļ���Ϣ	    			     
	tfileinfo=(FILINFO*)mymalloc(SRAMIN,sizeof(FILINFO));//�����ڴ�
    res=f_opendir(&tdir,(const TCHAR*)path); 	//��Ŀ¼ 
	if(res==FR_OK&&tfileinfo)
	{
		while(1)//��ѯ�ܵ���Ч�ļ���
		{
	        res=f_readdir(&tdir,tfileinfo);       		//��ȡĿ¼�µ�һ���ļ�  	 
	        if(res!=FR_OK||tfileinfo->fname[0]==0)break;//������/��ĩβ��,�˳�	 		 
			res=f_typetell((u8*)tfileinfo->fname);
			if((res&0XF0)==0X50)//ȡ����λ,�����ǲ���ͼƬ�ļ�	
			{
				rval++;//��Ч�ļ�������1
			}	    
		}  
	}  
	myfree(SRAMIN,tfileinfo);//�ͷ��ڴ�
	return rval;
}

int main(void)
{	
	u8 res;
 	DIR picdir;	 											//ͼƬĿ¼
	FILINFO *picfileinfo;							//�ļ���Ϣ 
	u8 *pname;												//��·�����ļ���
	u16 totpicnum; 										//ͼƬ�ļ�����
	u16 curindex;											//ͼƬ��ǰ����
	
	u8 pause=0;												//��ͣ���
	u8 t;
	u16 temp;
	u32 *picoffsettbl;								//ͼƬ�ļ�offset������ 

  
	HAL_Init();                     	//��ʼ��HAL��   
	Stm32_Clock_Init(360,25,2,8);   	//����ʱ��,180Mhz
	delay_init(180);                	//��ʼ����ʱ����
	uart_init(115200);              	//��ʼ��USART
	LED_Init();												//��ʼ����LED���ӵ�Ӳ���ӿ�
	
	
	
	SDRAM_Init();											//��ʼ��SDRAM 
	LCD_Init();												//��ʼ��LCD
	KEY_Init();												//��ʼ������
	TIM3_Init(50-1,9000-1);
	
	W25QXX_Init();										//��ʼ��W25Q256
	tp_dev.init();	
	W25QXX_Init();				    				//��ʼ��W25Q256
  WM8978_Init();				   			 		//��ʼ��WM8978
	WM8978_HPvol_Set(40,40);	    		//������������
	WM8978_SPKvol_Set(40);		    		//������������
 	my_mem_init(SRAMIN);		  				//��ʼ���ڲ��ڴ��
	my_mem_init(SRAMEX);							//��ʼ���ⲿ�ڴ��
	my_mem_init(SRAMCCM);							//��ʼ��CCM�ڴ�� 
	exfuns_init();										//Ϊfatfs��ر��������ڴ�  
 	f_mount(fs[0],"0:",1); 						//����SD�� 
 	f_mount(fs[1],"1:",1); 						//����FLASH.
 	f_mount(fs[2],"2:",1); 						//����NAND FLASH.
	POINT_COLOR=BLUE;      
	
	//EXTI_Init();                    //�ⲿ�жϳ�ʼ��
	
	while(font_init()) 																			//����ֿ�
	{	    
		LCD_ShowString(30,50,200,16,16,"Font Error!");
		delay_ms(200);				  
		LCD_Fill(30,50,240,66,WHITE);													//�����ʾ	     
		delay_ms(200);				  
	}  	 
 	Show_Str(30,50,200,16,"������STM32F4/F7������",16,0);				    	 
	Show_Str(30,70,200,16,"ͼƬ��ʾ����",16,0);				    	 
	Show_Str(30,90,200,16,"KEY0:NEXT KEY2:PREV",16,0);				    	 
	Show_Str(30,110,200,16,"KEY_UP:PAUSE",16,0);				    	 
	Show_Str(30,130,200,16,"����ԭ��@ALIENTEK",16,0);				    	 
	Show_Str(30,150,200,16,"2016��1��7��",16,0);
 	while(f_opendir(&picdir,"0:/PICTURE"))									//��ͼƬ�ļ���
 	{	    
		Show_Str(30,170,240,16,"PICTURE�ļ��д���!",16,0);
		delay_ms(200);				  
		LCD_Fill(30,170,240,186,WHITE);												//�����ʾ	     
		delay_ms(200);				  
	}  
	totpicnum=pic_get_tnum("0:/PICTURE"); 									//�õ�����Ч�ļ���
  	while(totpicnum==NULL)																//ͼƬ�ļ�Ϊ0		
 	{	    
		Show_Str(30,170,240,16,"û��ͼƬ�ļ�!",16,0);
		delay_ms(200);				  
		LCD_Fill(30,170,240,186,WHITE);												//�����ʾ	     
		delay_ms(200);				  
	} 
	picfileinfo=(FILINFO*)mymalloc(SRAMIN,sizeof(FILINFO));	//�����ڴ�
 	pname=mymalloc(SRAMIN,_MAX_LFN*2+1);										//Ϊ��·�����ļ��������ڴ�
 	picoffsettbl=mymalloc(SRAMIN,4*totpicnum);							//����4*totpicnum���ֽڵ��ڴ�,���ڴ��ͼƬ����
 	while(!picfileinfo||!pname||!picoffsettbl)							//�ڴ�������
 	{	    	
		Show_Str(30,170,240,16,"�ڴ����ʧ��!",16,0);
		delay_ms(200);				  
		LCD_Fill(30,170,240,186,WHITE);												//�����ʾ	     
		delay_ms(200);				  
	}  	
																													//��¼����
    res=f_opendir(&picdir,"0:/PICTURE"); 									//��Ŀ¼
	if(res==FR_OK)
	{
		curindex=0;																						//��ǰ����Ϊ0
		while(1)																							//ȫ����ѯһ��
		{
			temp=picdir.dptr;																		//��¼��ǰdptrƫ��
	        res=f_readdir(&picdir,picfileinfo);       			//��ȡĿ¼�µ�һ���ļ�
	        if(res!=FR_OK||picfileinfo->fname[0]==0)break;	//������/��ĩβ��,�˳�	 	 
			res=f_typetell((u8*)picfileinfo->fname);	
			if((res&0XF0)==0X50)																//ȡ����λ,�����ǲ���ͼƬ�ļ�	
			{
				picoffsettbl[curindex]=temp;											//��¼����
				curindex++;
			}	    
		} 
	}   
	Show_Str(30,170,240,16,"��ʼ��ʾ...",16,0); 
	delay_ms(1500);
	piclib_init();																					//��ʼ����ͼ	   	   
	curindex=0;																							//��0��ʼ��ʾ
  res=f_opendir(&picdir,(const TCHAR*)"0:/PICTURE"); 		//��Ŀ¼
	while(res==FR_OK)																				//�򿪳ɹ�
	{	
		audio_play();  //�����ɹ�����һ��
		dir_sdi(&picdir,picoffsettbl[curindex]);							//�ı䵱ǰĿ¼����	   
        res=f_readdir(&picdir,picfileinfo);       				//��ȡĿ¼�µ�һ���ļ�
        if(res!=FR_OK||picfileinfo->fname[0]==0)break;		//������/��ĩβ��,�˳�
		strcpy((char*)pname,"0:/PICTURE/");										//����·��(Ŀ¼)
		strcat((char*)pname,(const char*)picfileinfo->fname);	//���ļ������ں���
 		LCD_Clear(BLACK);
 		ai_load_picfile(pname,0,0,lcddev.width,lcddev.height,0);
																													//��ʾͼƬ    
		//Show_Str(2,2,lcddev.width,16,pname,16,1); 					//��ʾͼƬ����
		t=0;
		Curtain_Init();
		curtainFlag=0;
		lightFlag=0;
		co2Flag=0;
		defence=0;
		//count=0;
		while(1) 
		{
			if(tp_dev.x[0]>56&&tp_dev.x[0]<223&&tp_dev.y[0]>62&&tp_dev.y[0]<125){//���������򿪰�ť
				LED0=0;
				Show_Str(155,470,240,24,"����״̬����",24,0); 
			}
			if(tp_dev.x[0]>251&&tp_dev.x[0]<418&&tp_dev.y[0]>62&&tp_dev.y[0]<125){//���������رհ�ť
				LED0=1;
				Show_Str(155,470,240,24,"����״̬���ر�",24,0); 
			}
			if(tp_dev.x[0]>56&&tp_dev.x[0]<223&&tp_dev.y[0]>170&&tp_dev.y[0]<230){
				LED1=0;
				Show_Str(155,495,240,24,"���״̬����",24,0); 
			}
			if(tp_dev.x[0]>251&&tp_dev.x[0]<418&&tp_dev.y[0]>170&&tp_dev.y[0]<230){
				LED1=1;
				Show_Str(155,495,240,24,"���״̬���ر�",24,0); 
			}
			if(tp_dev.x[0]>56&&tp_dev.x[0]<223&&tp_dev.y[0]>275&&tp_dev.y[0]<335){
				Show_Str(155,570,240,24,"���״̬�����",24,0);
				defence=1;
			}
			if(tp_dev.x[0]>251&&tp_dev.x[0]<418&&tp_dev.y[0]>275&&tp_dev.y[0]<335){
				Show_Str(155,570,240,24,"���״̬������",24,0); 
				defence=0;
			}
			key=KEY_Scan(0);						//ɨ�谴��
			if(key==KEY0_PRES){
				if(curtainFlag==0){
					LED0=1;
					Show_Str(155,470,240,24,"����״̬���ر�",24,0);
					curtainFlag=1;
				}else{
					LED0=0;
					Show_Str(155,470,240,24,"����״̬����",24,0);
					curtainFlag=0;
				}
			}
			if(key==KEY1_PRES){
				if(lightFlag==0){
					LED1=1;
					Show_Str(155,495,240,24,"���״̬���ر�",24,0);
					lightFlag=1;
				}else{
					LED1=0;
					Show_Str(155,495,240,24,"���״̬����",24,0);
					lightFlag=0;
				}
			}
			if(key==KEY2_PRES){
				if(co2Flag==0){
					
					Show_Str(155,520,240,24,"ú����ȫ����ȫ",24,0);
					co2Flag=1;
				}else{
					LED0=0;
					Show_Str(155,520,240,24,"ú����ȫ��Σ��",24,0);
					Show_Str(155,470,240,24,"����״̬����",24,0);
					co2Flag=0;
				}
			}
			if( (defence==1&&co2Flag==0) || (defence==1&&curtainFlag==0) ){//����״̬��ú��Σ�գ������ر�ʱ���������������ƻ�������ֹͣ���ž���
				audio_play();
			}
			if(key==WKUP_PRES){
				pause=!pause;
				LED1=!pause; 							//��ͣ��ʱ��LED1��.  
			}
			if(pause==0)t++;
			delay_ms(10); 
		}					    
		res=0;  
	} 							    
	myfree(SRAMIN,picfileinfo);			//�ͷ��ڴ�						   		    
	myfree(SRAMIN,pname);						//�ͷ��ڴ�			    
	myfree(SRAMIN,picoffsettbl);		//�ͷ��ڴ�

}



