#include "exti.h"
#include "delay.h"
#include "led.h"
#include "key.h"
#include "lcd.h"
#include "touch.h"
#include "text.h"
//////////////////////////////////////////////////////////////////////////////////	 
//本程序只供学习使用，未经作者许可，不得用于其它任何用途
//ALIENTEK STM32F429开发板
//外部中断驱动代码	   
//正点原子@ALIENTEK
//技术论坛:www.openedv.com
//创建日期:2016/1/5
//版本：V1.0
//版权所有，盗版必究。
//Copyright(C) 广州市星翼电子科技有限公司 2014-2024
//All rights reserved									  
////////////////////////////////////////////////////////////////////////////////// 	

//外部中断初始化
void EXTI_Init(void)
{
    GPIO_InitTypeDef GPIO_Initure;
	
	 __HAL_RCC_GPIOA_CLK_ENABLE();               //开启GPIOA时钟
    __HAL_RCC_GPIOC_CLK_ENABLE();               //开启GPIOC时钟
    __HAL_RCC_GPIOH_CLK_ENABLE();               //开启GPIOH时钟
    
	  GPIO_Initure.Pin=GPIO_PIN_7;            //PH7
    GPIO_Initure.Mode=GPIO_MODE_IT_RISING;  //??
    GPIO_Initure.Pull=GPIO_PULLUP;        //?????,????
    GPIO_Initure.Speed=GPIO_SPEED_HIGH;     //??
    HAL_GPIO_Init(GPIOH,&GPIO_Initure);     //???
	
//		//PH7
//		GPIO_Initure.Pin=GPIO_PIN_7;            //PH7
//		GPIO_Initure.Mode=GPIO_MODE_INPUT;      //输入
//		HAL_GPIO_Init(GPIOH,&GPIO_Initure);     //初始化
		
    HAL_NVIC_SetPriority(EXTI9_5_IRQn,2,0);       //??????2,?????0
    HAL_NVIC_EnableIRQ(EXTI9_5_IRQn);             //?????0	

		Show_Str(30,50,200,16,"lulalulalllllllllllllllllllllllllllllllllll",16,0);
	
	GPIO_Initure.Pin=GPIO_PIN_13;               //PC13
    GPIO_Initure.Mode=GPIO_MODE_IT_FALLING;     //下降沿触发、、
    GPIO_Initure.Pull=GPIO_PULLUP;
    HAL_GPIO_Init(GPIOC,&GPIO_Initure);
	
	//中断线13-PC13
    HAL_NVIC_SetPriority(EXTI15_10_IRQn,2,3);   //抢占优先级为2，子优先级为3
    HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);         //使能中断线13  
    
//    GPIO_Initure.Pin=PEN;                //PA0
//    GPIO_Initure.Mode=GPIO_MODE_IT_RISING;      //上升沿触发
//    GPIO_Initure.Pull=GPIO_PULLDOWN;
	
   // HAL_GPIO_Init(GPIOA,&GPIO_Initure);
    
//    GPIO_Initure.Pin=GPIO_PIN_13;               //PC13
//    GPIO_Initure.Mode=GPIO_MODE_IT_FALLING;     //下降沿触发、、
//    GPIO_Initure.Pull=GPIO_PULLUP;
//    HAL_GPIO_Init(GPIOC,&GPIO_Initure);
    
//    GPIO_Initure.Pin=GPIO_PIN_2|GPIO_PIN_3;     //PH2,3
//    HAL_GPIO_Init(GPIOH,&GPIO_Initure);
    
//    //中断线0-PA0
//    HAL_NVIC_SetPriority(EXTI0_IRQn,2,0);       //抢占优先级为2，子优先级为0
//    HAL_NVIC_EnableIRQ(EXTI0_IRQn);             //使能中断线0
    
    //中断线2-PH2
//    HAL_NVIC_SetPriority(EXTI2_IRQn,2,1);       //抢占优先级为2，子优先级为1
//    HAL_NVIC_EnableIRQ(EXTI2_IRQn);             //使能中断线2
    
    //中断线3-PH3
//    HAL_NVIC_SetPriority(EXTI3_IRQn,2,2);       //抢占优先级为2，子优先级为2
//    HAL_NVIC_EnableIRQ(EXTI3_IRQn);             //使能中断线2
    
//    //中断线13-PC13
//    HAL_NVIC_SetPriority(EXTI15_10_IRQn,2,3);   //抢占优先级为2，子优先级为3
//    HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);         //使能中断线13  
}


//中断服务函数
//void EXTI0_IRQHandler(void)
//{
//    HAL_GPIO_EXTI_IRQHandler(PEN);//调用中断处理公用函数
//}

void EXTI9_5_IRQHandler(void)
{
	
  //HAL_GPIO_EXTI_IRQHandler(PEN);//??????????
}

void EXTI15_10_IRQHandler(void)
{
    //HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_13);//调用中断处理公用函数
}

//中断服务程序中需要做的事情
//在HAL库中所有的外部中断服务函数都会调用此函数
//GPIO_Pin:中断引脚号
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
//    delay_ms(100);      //消抖
//	switch(GPIO_Pin)
//    {
//        case PEN:
//					Show_Str(30,50,200,16,"haha",16,0);
//					tp_dev.scan(0);
//	while(tp_dev.x[0]==65535){
//	tp_dev.scan(0);
//	}
//	if(tp_dev.x[0]>56&&tp_dev.x[0]<223&&tp_dev.y[0]>62&&tp_dev.y[0]<125){//按到窗帘打开按钮
//				LED0=0;
//				Show_Str(155,470,240,24,"窗帘状态：打开",24,0); 
//			}
//			if(tp_dev.x[0]>251&&tp_dev.x[0]<418&&tp_dev.y[0]>62&&tp_dev.y[0]<125){//按到窗帘关闭按钮
//				LED0=1;
//				Show_Str(155,470,240,24,"窗帘状态：关闭",24,0); 
//			}
//			if(tp_dev.x[0]>56&&tp_dev.x[0]<223&&tp_dev.y[0]>170&&tp_dev.y[0]<230){
//				LED1=0;
//				Show_Str(155,495,240,24,"电灯状态：打开",24,0); 
//			}
//			if(tp_dev.x[0]>251&&tp_dev.x[0]<418&&tp_dev.y[0]>170&&tp_dev.y[0]<230){
//				LED1=1;
//				Show_Str(155,495,240,24,"电灯状态：关闭",24,0); 
//			}
			
//    }

}
