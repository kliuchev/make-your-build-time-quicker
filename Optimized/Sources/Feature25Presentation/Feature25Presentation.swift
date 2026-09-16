import Feature25Domain
import Feature25Data

public enum Feature25PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature25DomainModel = Feature25DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
