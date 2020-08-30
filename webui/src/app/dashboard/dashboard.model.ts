export class LineSeries {
  name: string;
  value: string;
}

export class LineModel {
  name: string;
  series: LineSeries[];
  status?: string;
}
