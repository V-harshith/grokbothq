import newsJson from "../../content/news.json";

export type NewsItem = {
  date: string;
  title: string;
  source: string;
  url: string;
  summary: string;
};

export const news: NewsItem[] = newsJson as NewsItem[];
