#include "exti.h"
#include "delay.h"
#include "led.h"
#include "key.h"
#include "lcd.h"
#include "touch.h"
#include "text.h"
//////////////////////////////////////////////////////////////////////////////////	 
//������ֻ��ѧϰʹ�ã�δ��������ɣ��������������κ���;
//ALIENTEK STM32F429������
//�ⲿ�ж���������	   
//����ԭ��@ALIENTEK
//������̳:www.openedv.com
//��������:2016/1/5
//�汾��V1.0
//��Ȩ���У�����ؾ���
//Copyright(C) ������������ӿƼ����޹�˾ 2014-2024
//All rights reserved									  
////////////////////////////////////////////////////////////////////////////////// 	

//�ⲿ�жϳ�ʼ��
void EXTI_Init(void)
{
    GPIO_InitTypeDef GPIO_Initure;
	
	 __HAL_RCC_GPIOA_CLK_ENABLE();               //����GPIOAʱ��
    __HAL_RCC_GPIOC_CLK_ENABLE();               //����GPIOCʱ��
    __HAL_RCC_GPIOH_CLK_ENABLE();               //����GPIOHʱ��
    
	  GPIO_Initure.Pin=GPIO_PIN_7;            //PH7
    GPIO_Initure.Mode=GPIO_MODE_IT_RISING;  //??
    GPIO_Initure.Pull=GPIO_PULLUP;        //?????,????
    GPIO_Initure.Speed=GPIO_SPEED_HIGH;     //??
    HAL_GPIO_Init(GPIOH,&GPIO_Initure);     //???
	
//		//PH7
//		GPIO_Initure.Pin=GPIO_PIN_7;            //PH7
//		GPIO_Initure.Mode=GPIO_MODE_INPUT;      //����
//		HAL_GPIO_Init(GPIOH,&GPIO_Initure);     //��ʼ��
		
    HAL_NVIC_SetPriority(EXTI9_5_IRQn,2,0);       //??????2,?????0
    HAL_NVIC_EnableIRQ(EXTI9_5_IRQn);             //?????0	

		Show_Str(30,50,200,16,"lulalulalllllllllllllllllllllllllllllllllll",16,0);
	
	GPIO_Initure.Pin=GPIO_PIN_13;               //PC13
    GPIO_Initure.Mode=GPIO_MODE_IT_FALLING;     //�½��ش�������
    GPIO_Initure.Pull=GPIO_PULLUP;
    HAL_GPIO_Init(GPIOC,&GPIO_Initure);
	
	//�ж���13-PC13
    HAL_NVIC_SetPriority(EXTI15_10_IRQn,2,3);   //��ռ���ȼ�Ϊ2�������ȼ�Ϊ3
    HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);         //ʹ���ж���13  
    
//    GPIO_Initure.Pin=PEN;                //PA0
//    GPIO_Initure.Mode=GPIO_MODE_IT_RISING;      //�����ش���
//    GPIO_Initure.Pull=GPIO_PULLDOWN;
	
   // HAL_GPIO_Init(GPIOA,&GPIO_Initure);
    
//    GPIO_Initure.Pin=GPIO_PIN_13;               //PC13
//    GPIO_Initure.Mode=GPIO_MODE_IT_FALLING;     //�½��ش�������
//    GPIO_Initure.Pull=GPIO_PULLUP;
//    HAL_GPIO_Init(GPIOC,&GPIO_Initure);
    
//    GPIO_Initure.Pin=GPIO_PIN_2|GPIO_PIN_3;     //PH2,3
//    HAL_GPIO_Init(GPIOH,&GPIO_Initure);
    
//    //�ж���0-PA0
//    HAL_NVIC_SetPriority(EXTI0_IRQn,2,0);       //��ռ���ȼ�Ϊ2�������ȼ�Ϊ0
//    HAL_NVIC_EnableIRQ(EXTI0_IRQn);             //ʹ���ж���0
    
    //�ж���2-PH2
//    HAL_NVIC_SetPriority(EXTI2_IRQn,2,1);       //��ռ���ȼ�Ϊ2�������ȼ�Ϊ1
//    HAL_NVIC_EnableIRQ(EXTI2_IRQn);             //ʹ���ж���2
    
    //�ж���3-PH3
//    HAL_NVIC_SetPriority(EXTI3_IRQn,2,2);       //��ռ���ȼ�Ϊ2�������ȼ�Ϊ2
//    HAL_NVIC_EnableIRQ(EXTI3_IRQn);             //ʹ���ж���2
    
//    //�ж���13-PC13
//    HAL_NVIC_SetPriority(EXTI15_10_IRQn,2,3);   //��ռ���ȼ�Ϊ2�������ȼ�Ϊ3
//    HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);         //ʹ���ж���13  
}


//�жϷ�����
//void EXTI0_IRQHandler(void)
//{
//    HAL_GPIO_EXTI_IRQHandler(PEN);//�����жϴ����ú���
//}

void EXTI9_5_IRQHandler(void)
{
	
  //HAL_GPIO_EXTI_IRQHandler(PEN);//??????????
}

void EXTI15_10_IRQHandler(void)
{
    //HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_13);//�����жϴ����ú���
}

//�жϷ����������Ҫ��������
//��HAL�������е��ⲿ�жϷ�����������ô˺���
//GPIO_Pin:�ж����ź�
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
//    delay_ms(100);      //����
//	switch(GPIO_Pin)
//    {
//        case PEN:
//					Show_Str(30,50,200,16,"haha",16,0);
//					tp_dev.scan(0);
//	while(tp_dev.x[0]==65535){
//	tp_dev.scan(0);
//	}
//	if(tp_dev.x[0]>56&&tp_dev.x[0]<223&&tp_dev.y[0]>62&&tp_dev.y[0]<125){//���������򿪰�ť
//				LED0=0;
//				Show_Str(155,470,240,24,"����״̬����",24,0); 
//			}
//			if(tp_dev.x[0]>251&&tp_dev.x[0]<418&&tp_dev.y[0]>62&&tp_dev.y[0]<125){//���������رհ�ť
//				LED0=1;
//				Show_Str(155,470,240,24,"����״̬���ر�",24,0); 
//			}
//			if(tp_dev.x[0]>56&&tp_dev.x[0]<223&&tp_dev.y[0]>170&&tp_dev.y[0]<230){
//				LED1=0;
//				Show_Str(155,495,240,24,"���״̬����",24,0); 
//			}
//			if(tp_dev.x[0]>251&&tp_dev.x[0]<418&&tp_dev.y[0]>170&&tp_dev.y[0]<230){
//				LED1=1;
//				Show_Str(155,495,240,24,"���״̬���ر�",24,0); 
//			}
			
//    }

}
