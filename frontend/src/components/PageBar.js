

export default function PageBar(props) {
  const {forward, back, page, limit, count} = props;
  const offset = limit * (page - 1);
  const start = count > 0 ? offset+1 : 0;
  const end = offset+limit < count ? offset+limit : count;
  return <>
    <p>
      Showing {start}-{end} of {count}
    </p>
    {page > 1 ? <>
      <span onClick={back}>Previous</span>
    </> : ''}
    <span className='mx-3'>{page}</span>
    {page * limit < count ? <>
      <span onClick={forward}>Next</span>
    </> : ''}
  </>;
}
