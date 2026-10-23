import {z} from 'zod';

export const schema = z.object({
  salam: z.string(),
  ayat: z.string(),
  terjemahan: z.string(),
  rujukan: z.string(),
  doa1: z.string(),
  doa2Pembuka: z.string(),
  doa2Kata: z.tuple([z.string(), z.string(), z.string()]),
  doa2Penutup: z.string(),
  muzik: z.boolean(),
});

export type Props = z.infer<typeof schema>;

export const defaultProps: Props = {
  salam: 'SALAM JUMAAT',
  ayat: 'وَتَعَاوَنُوا عَلَى الْبِرِّ وَالتَّقْوَىٰ',
  terjemahan: 'Dan hendaklah kamu bertolong-tolongan untuk membuat kebajikan dan bertakwa.',
  rujukan: 'Surah Al-Ma’idah, ayat 2',
  doa1: 'Ya Allah, berkatilah setiap usaha kami dalam membangunkan negeri Melaka.',
  doa2Pembuka: 'Kurniakan',
  doa2Kata: ['kemajuan', 'kemakmuran', 'kesejahteraan'],
  doa2Penutup: 'buat seluruh rakyatnya.',
  muzik: true,
};
