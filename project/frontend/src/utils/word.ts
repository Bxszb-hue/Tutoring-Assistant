import { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, AlignmentType } from 'docx'

export const generateWarningWordReport = async (): Promise<Blob> => {
  const doc = new Document({
    sections: [{
      properties: {},
      children: [
        new Paragraph({
          text: '学业预警报告',
          heading: HeadingLevel.HEADING_1,
          alignment: AlignmentType.CENTER
        }),
        
        new Paragraph({
          text: '统计周期：2024年9月',
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 }
        }),
        
        new Paragraph({
          text: '一、预警类型分布',
          heading: HeadingLevel.HEADING_2,
          spacing: { after: 100 }
        }),
        
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('预警类型')] }),
                new TableCell({ children: [new Paragraph('数量')] }),
                new TableCell({ children: [new Paragraph('占比')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('学业预警')] }),
                new TableCell({ children: [new Paragraph('12')] }),
                new TableCell({ children: [new Paragraph('48%')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('心理预警')] }),
                new TableCell({ children: [new Paragraph('8')] }),
                new TableCell({ children: [new Paragraph('32%')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('日常预警')] }),
                new TableCell({ children: [new Paragraph('5')] }),
                new TableCell({ children: [new Paragraph('20%')] })
              ]
            })
          ]
        }),
        
        new Paragraph({
          text: '',
          spacing: { after: 100 }
        }),
        
        new Paragraph({
          text: '二、预警等级分布',
          heading: HeadingLevel.HEADING_2,
          spacing: { after: 100 }
        }),
        
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('预警等级')] }),
                new TableCell({ children: [new Paragraph('人数')] }),
                new TableCell({ children: [new Paragraph('占比')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('轻度预警')] }),
                new TableCell({ children: [new Paragraph('15')] }),
                new TableCell({ children: [new Paragraph('60%')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('中度预警')] }),
                new TableCell({ children: [new Paragraph('7')] }),
                new TableCell({ children: [new Paragraph('28%')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('重度预警')] }),
                new TableCell({ children: [new Paragraph('3')] }),
                new TableCell({ children: [new Paragraph('12%')] })
              ]
            })
          ]
        }),
        
        new Paragraph({
          text: '',
          spacing: { after: 100 }
        }),
        
        new Paragraph({
          text: '三、预警学生名单',
          heading: HeadingLevel.HEADING_2,
          spacing: { after: 100 }
        }),
        
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('姓名')] }),
                new TableCell({ children: [new Paragraph('学号')] }),
                new TableCell({ children: [new Paragraph('预警类型')] }),
                new TableCell({ children: [new Paragraph('预警等级')] }),
                new TableCell({ children: [new Paragraph('预警原因')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('张伟')] }),
                new TableCell({ children: [new Paragraph('2021001')] }),
                new TableCell({ children: [new Paragraph('学业预警')] }),
                new TableCell({ children: [new Paragraph('中度')] }),
                new TableCell({ children: [new Paragraph('连续两门课程挂科')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('李明')] }),
                new TableCell({ children: [new Paragraph('2021002')] }),
                new TableCell({ children: [new Paragraph('学业预警')] }),
                new TableCell({ children: [new Paragraph('轻度')] }),
                new TableCell({ children: [new Paragraph('多门课程成绩下滑')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('王芳')] }),
                new TableCell({ children: [new Paragraph('2021003')] }),
                new TableCell({ children: [new Paragraph('心理预警')] }),
                new TableCell({ children: [new Paragraph('中度')] }),
                new TableCell({ children: [new Paragraph('近期情绪波动较大')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('周杰')] }),
                new TableCell({ children: [new Paragraph('2022002')] }),
                new TableCell({ children: [new Paragraph('学业预警')] }),
                new TableCell({ children: [new Paragraph('重度')] }),
                new TableCell({ children: [new Paragraph('连续挂科')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('王磊')] }),
                new TableCell({ children: [new Paragraph('2021003')] }),
                new TableCell({ children: [new Paragraph('日常预警')] }),
                new TableCell({ children: [new Paragraph('重度')] }),
                new TableCell({ children: [new Paragraph('违纪与晚归')] })
              ]
            })
          ]
        }),
        
        new Paragraph({
          text: '',
          spacing: { after: 100 }
        }),
        
        new Paragraph({
          text: '四、预警处理情况',
          heading: HeadingLevel.HEADING_2,
          spacing: { after: 100 }
        }),
        
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('状态')] }),
                new TableCell({ children: [new Paragraph('人数')] }),
                new TableCell({ children: [new Paragraph('占比')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('已处理')] }),
                new TableCell({ children: [new Paragraph('18')] }),
                new TableCell({ children: [new Paragraph('72%')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('待处理')] }),
                new TableCell({ children: [new Paragraph('7')] }),
                new TableCell({ children: [new Paragraph('28%')] })
              ]
            })
          ]
        }),
        
        new Paragraph({
          text: '',
          spacing: { after: 100 }
        }),
        
        new Paragraph({
          text: '五、建议措施',
          heading: HeadingLevel.HEADING_2,
          spacing: { after: 100 }
        }),
        
        new Paragraph({
          children: [
            new TextRun('1. 及时与预警学生沟通，了解具体情况\n'),
            new TextRun('2. 针对学业预警学生，制定个性化帮扶计划\n'),
            new TextRun('3. 针对心理预警学生，建议预约心理咨询\n'),
            new TextRun('4. 定期跟踪预警学生的状态变化')
          ]
        })
      ]
    }]
  })
  
  return await Packer.toBlob(doc)
}

export const generateWorkWordReport = async (warningData: any = null): Promise<Blob> => {
  const doc = new Document({
    sections: [{
      properties: {},
      children: [
        new Paragraph({
          text: '辅导员工作报告',
          heading: HeadingLevel.HEADING_1,
          alignment: AlignmentType.CENTER
        }),
        
        new Paragraph({
          text: '统计周期：2024年9月',
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 }
        }),
        
        new Paragraph({
          text: '一、工作概况',
          heading: HeadingLevel.HEADING_2,
          spacing: { after: 100 }
        }),
        
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('项目')] }),
                new TableCell({ children: [new Paragraph('数值')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('负责学生数')] }),
                new TableCell({ children: [new Paragraph('18')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('谈心谈话')] }),
                new TableCell({ children: [new Paragraph('35人次')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('家访/家校沟通')] }),
                new TableCell({ children: [new Paragraph('8次')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('处理事务')] }),
                new TableCell({ children: [new Paragraph('93件')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('组织活动')] }),
                new TableCell({ children: [new Paragraph('6场')] })
              ]
            })
          ]
        }),
        
        new Paragraph({
          text: '',
          spacing: { after: 100 }
        }),
        
        new Paragraph({
          text: '二、预警管理情况',
          heading: HeadingLevel.HEADING_2,
          spacing: { after: 100 }
        }),
        
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('预警类型')] }),
                new TableCell({ children: [new Paragraph('总数')] }),
                new TableCell({ children: [new Paragraph('已处理')] }),
                new TableCell({ children: [new Paragraph('待处理')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('学业预警')] }),
                new TableCell({ children: [new Paragraph('12')] }),
                new TableCell({ children: [new Paragraph('8')] }),
                new TableCell({ children: [new Paragraph('4')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('心理预警')] }),
                new TableCell({ children: [new Paragraph('8')] }),
                new TableCell({ children: [new Paragraph('6')] }),
                new TableCell({ children: [new Paragraph('2')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('日常预警')] }),
                new TableCell({ children: [new Paragraph('5')] }),
                new TableCell({ children: [new Paragraph('4')] }),
                new TableCell({ children: [new Paragraph('1')] })
              ]
            })
          ]
        }),
        
        new Paragraph({
          text: '',
          spacing: { after: 100 }
        }),
        
        new Paragraph({
          text: '三、事务办理统计',
          heading: HeadingLevel.HEADING_2,
          spacing: { after: 100 }
        }),
        
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('事务类型')] }),
                new TableCell({ children: [new Paragraph('数量')] }),
                new TableCell({ children: [new Paragraph('完成率')] }),
                new TableCell({ children: [new Paragraph('平均时长')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('请假')] }),
                new TableCell({ children: [new Paragraph('45')] }),
                new TableCell({ children: [new Paragraph('100%')] }),
                new TableCell({ children: [new Paragraph('1.5天')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('开具证明')] }),
                new TableCell({ children: [new Paragraph('28')] }),
                new TableCell({ children: [new Paragraph('96%')] }),
                new TableCell({ children: [new Paragraph('2.0天')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('补办证件')] }),
                new TableCell({ children: [new Paragraph('12')] }),
                new TableCell({ children: [new Paragraph('100%')] }),
                new TableCell({ children: [new Paragraph('1.0天')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('其他事务')] }),
                new TableCell({ children: [new Paragraph('8')] }),
                new TableCell({ children: [new Paragraph('88%')] }),
                new TableCell({ children: [new Paragraph('3.0天')] })
              ]
            })
          ]
        }),
        
        new Paragraph({
          text: '',
          spacing: { after: 100 }
        }),
        
        new Paragraph({
          text: '四、活动组织记录',
          heading: HeadingLevel.HEADING_2,
          spacing: { after: 100 }
        }),
        
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('活动名称')] }),
                new TableCell({ children: [new Paragraph('类型')] }),
                new TableCell({ children: [new Paragraph('参与人次')] }),
                new TableCell({ children: [new Paragraph('日期')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('安全教育主题班会')] }),
                new TableCell({ children: [new Paragraph('主题班会')] }),
                new TableCell({ children: [new Paragraph('18')] }),
                new TableCell({ children: [new Paragraph('2024-09-05')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('心理健康讲座')] }),
                new TableCell({ children: [new Paragraph('主题班会')] }),
                new TableCell({ children: [new Paragraph('18')] }),
                new TableCell({ children: [new Paragraph('2024-09-12')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('迎新座谈会')] }),
                new TableCell({ children: [new Paragraph('班级活动')] }),
                new TableCell({ children: [new Paragraph('18')] }),
                new TableCell({ children: [new Paragraph('2024-09-01')] })
              ]
            }),
            new TableRow({
              children: [
                new TableCell({ children: [new Paragraph('中秋晚会')] }),
                new TableCell({ children: [new Paragraph('班级活动')] }),
                new TableCell({ children: [new Paragraph('18')] }),
                new TableCell({ children: [new Paragraph('2024-09-17')] })
              ]
            })
          ]
        }),
        
        new Paragraph({
          text: '',
          spacing: { after: 100 }
        }),
        
        new Paragraph({
          text: '五、月度总结',
          heading: HeadingLevel.HEADING_2,
          spacing: { after: 100 }
        }),
        
        new Paragraph({
          text: '本月工作进展顺利，各项指标良好。预警管理方面，共处理预警25起，处理率达到72%，建议加快待处理预警的跟进速度，关注重度预警学生。事务办理效率较高，平均办理时长2.1天，满意度95%。活动组织丰富多样，有效增强了班级凝聚力。'
        })
      ]
    }]
  })
  
  return await Packer.toBlob(doc)
}

export const downloadBlob = (blob: Blob, filename: string) => {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
