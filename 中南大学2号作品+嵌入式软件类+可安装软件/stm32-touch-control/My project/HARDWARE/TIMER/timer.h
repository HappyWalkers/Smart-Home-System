#ifndef _TIMER_H
#define _TIMER_H
#include "sys.h"
static	u8 curtainFlag;
static	u8 lightFlag;
static	u8 co2Flag;
static	u8 doorFlag;
static	u8 defence;
static	u8 count;
static  u8 key;														//��ֵ
//////////////////////////////////////////////////////////////////////////////////	 
//������ֻ��ѧϰʹ�ã�δ��������ɣ��������������κ���;
//ALIENTEK STM32F429������
//��ʱ����������	   
//����ԭ��@ALIENTEK
//������̳:www.openedv.com
//��������:2016/1/6
//�汾��V1.0
//��Ȩ���У�����ؾ���
//Copyright(C) ������������ӿƼ����޹�˾ 2014-2024
//All rights reserved									  
////////////////////////////////////////////////////////////////////////////////// 	
extern TIM_HandleTypeDef TIM3_Handler;      //��ʱ����� 

void TIM3_Init(u16 arr,u16 psc);
#endif

