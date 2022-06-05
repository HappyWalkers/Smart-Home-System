#include "timer.h"
#include "led.h"
#include "touch.h"
#include "key.h"
#include "string.h"
#include "lcd.h"
#include "text.h"
#include "wavplay.h"
//////////////////////////////////////////////////////////////////////////////////	 
//������ֻ��ѧϰʹ�ã�δ��������ɣ��������������κ���;
//ALIENTEK STM32F429������
//��ʱ���ж���������	   
//����ԭ��@ALIENTEK
//������̳:www.openedv.com
//��������:2016/1/6
//�汾��V1.0
//��Ȩ���У�����ؾ���
//Copyright(C) ������������ӿƼ����޹�˾ 2014-2024
//All rights reserved									  
////////////////////////////////////////////////////////////////////////////////// 	



TIM_HandleTypeDef TIM3_Handler;      //��ʱ����� 

//ͨ�ö�ʱ��3�жϳ�ʼ��
//arr���Զ���װֵ��
//psc��ʱ��Ԥ��Ƶ��
//��ʱ�����ʱ����㷽��:Tout=((arr+1)*(psc+1))/Ft us.
//Ft=��ʱ������Ƶ��,��λ:Mhz
//����ʹ�õ��Ƕ�ʱ��3!(��ʱ��3����APB1�ϣ�ʱ��ΪHCLK/2)
void TIM3_Init(u16 arr,u16 psc)
{  
    TIM3_Handler.Instance=TIM3;                          //ͨ�ö�ʱ��3
    TIM3_Handler.Init.Prescaler=psc;                     //��Ƶϵ��
    TIM3_Handler.Init.CounterMode=TIM_COUNTERMODE_UP;    //���ϼ�����
    TIM3_Handler.Init.Period=arr;                        //�Զ�װ��ֵ
    TIM3_Handler.Init.ClockDivision=TIM_CLOCKDIVISION_DIV1;//ʱ�ӷ�Ƶ����
    HAL_TIM_Base_Init(&TIM3_Handler);
    
    HAL_TIM_Base_Start_IT(&TIM3_Handler); //ʹ�ܶ�ʱ��3�Ͷ�ʱ��3�����жϣ�TIM_IT_UPDATE   
}


//��ʱ���ײ�����������ʱ�ӣ������ж����ȼ�
//�˺����ᱻHAL_TIM_Base_Init()��������
void HAL_TIM_Base_MspInit(TIM_HandleTypeDef *htim)
{
    if(htim->Instance==TIM3)
	{
		__HAL_RCC_TIM3_CLK_ENABLE();            //ʹ��TIM3ʱ��
		HAL_NVIC_SetPriority(TIM3_IRQn,1,3);    //�����ж����ȼ�����ռ���ȼ�1�������ȼ�3
		HAL_NVIC_EnableIRQ(TIM3_IRQn);          //����ITM3�ж�   
	}
}


//��ʱ��3�жϷ�����
void TIM3_IRQHandler(void)
{
    HAL_TIM_IRQHandler(&TIM3_Handler);
}


//�ص���������ʱ���жϷ���������
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
    tp_dev.scan(0);
	if(tp_dev.x[0]>56&&tp_dev.x[0]<223&&tp_dev.y[0]>62&&tp_dev.y[0]<125){//���������򿪰�ť
				LED0=1;
				Show_Str(155,470,240,24,"����״̬����",24,0); 
			}
			if(tp_dev.x[0]>251&&tp_dev.x[0]<418&&tp_dev.y[0]>62&&tp_dev.y[0]<125){//���������رհ�ť
				LED0=0;
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
}
