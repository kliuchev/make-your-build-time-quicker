import Feature22Domain
import Feature22Data

public enum Feature22PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature22DomainModel = Feature22DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
