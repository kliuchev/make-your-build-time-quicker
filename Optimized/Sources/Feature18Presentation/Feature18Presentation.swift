import Feature18Domain
import Feature18Data

public enum Feature18PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature18DomainModel = Feature18DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
