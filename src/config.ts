export const SITE = {
  website: "https://gustavosalvini.com.ar/", // replace this with your deployed domain
  author: "Gustavo Adrián Salvini",
  profile: "https://gustavosalvini.com.ar/",
  desc: "A personal playground for digital exploration by Gustavo Adrián Salvini.",
  title: "Gustavo Adrián Salvini",
  altTitle: "The Perks of Sharing Knowledge",
  ogImage: "gustavosalvini-og.jpg",
  lightAndDarkMode: true,
  postPerIndex: 4,
  postPerPage: 4,
  scheduledPostMargin: 15 * 60 * 1000, // 15 minutes
  showArchives: true,
  showBackButton: true, // show back button in post detail
  editPost: {
    enabled: false,
    text: "Suggest Changes",
    url: "https://github.com/guspatagonico/gustavosalvini-astro-blog/edit/main/",
  },
  dynamicOgImage: true,
  lang: "en", // html lang code. Set this empty and default will be "en"
  timezone: "America/Argentina/Buenos_Aires", // Default global timezone (IANA format) https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
} as const;
